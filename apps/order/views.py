import logging
from datetime import timedelta

from django.db import transaction, IntegrityError
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST

from apps.agent.models import Agent
from apps.order.enums import DelayResponseCodeEnum
from apps.order.models import Order, OrderDelayReport, DelayReportAction, DelayReportState
from apps.order.serializers import OrderSerializer, ReportOrderResponseSerializer, OrderDelayReportSerializer
from apps.order.utils import renew_shipment_time
from apps.trip.models import TripState

logger = logging.getLogger(__name__)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("delay_reports", "trip")
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    @action(
        detail=True,
        methods=['GET'],
        url_path='report-delay',
        url_name="Report a delay for an order."
    )
    def delay(self, request, **kwargs):
        order: Order = self.get_object()
        if order.deliver_at > timezone.now():
            return Response(data={"message": "You cannot report a delay before the delivery time."})

        trip = hasattr(order, "trip") and order.trip
        if trip and trip.status in [TripState.ASSIGNED, TripState.AT_VENDOR, TripState.PICKED]:
            new_shipment_time_min: int = renew_shipment_time(order.id)
            new_shipment_datetime = timezone.now() + timedelta(minutes=new_shipment_time_min)
            delay_shipment_sec = int(new_shipment_datetime.timestamp() - order.deliver_at.timestamp())
            delay_shipment_min = int(delay_shipment_sec / 60) or 1  # Min 1 minutes
            with transaction.atomic():
                order.deliver_at = new_shipment_datetime
                order.save(update_fields=["deliver_at"])
                report_delay = OrderDelayReport.objects.create(
                    order=order,
                    action=DelayReportAction.SHIPPING_TIME_UPDATED,
                    vendor=order.vendor,
                    delay=delay_shipment_min
                )
            message = "Shipment time has been updated."
            code = DelayResponseCodeEnum.SHIPMENT_TIME_UPDATED

        elif report_delay := OrderDelayReport.objects.filter(
                order=order,
                state=DelayReportState.WAITING_FOR_AGENT
        ).first():
            message = "Already the order delay was submitted."
            code = DelayResponseCodeEnum.ALREADY_SUBMITTED

        else:
            report_delay = OrderDelayReport.objects.create(
                order=order,
                action=DelayReportAction.INSERTED_INTO_QUEUE,
                vendor=order.vendor,
                delay=int(int(timezone.now().timestamp() - order.deliver_at.timestamp()) / 60)
            )
            message = "Delay report has been submitted."
            code = DelayResponseCodeEnum.SHIPMENT_TIME_UPDATED

        response_serializer = ReportOrderResponseSerializer(data={
            "order": self.serializer_class(order).data,
            "report": OrderDelayReportSerializer(report_delay).data,
            "code": code,
            "message": message}
        )
        response_serializer.is_valid(raise_exception=True)
        return Response(data=response_serializer.data, status=HTTP_200_OK)

    @action(
        detail=False,
        methods=['GET'],
        url_path='delay-assign/(?P<agent_id>[^/.]+)',
        url_name="Assign FIFO delay to agent"
    )
    def assign(self, request, agent_id):
        if not Agent.objects.filter(id=agent_id).exists():
            message = "Agent id not exists!"
            code = 1
            order_report = None
            status = HTTP_404_NOT_FOUND
        else:
            order_is_ready_to_be_assigned_subquery = OrderDelayReport.objects.filter(
                state=DelayReportState.WAITING_FOR_AGENT
            ).exclude(state=DelayReportState.ASSIGNED_TO_VENDOR, agent_id=agent_id).order_by("id")
            try:
                is_assigned = OrderDelayReport.objects.filter(
                    id=order_is_ready_to_be_assigned_subquery.values("id")[:1]).update(
                    agent_id=agent_id,
                    assigned_at=timezone.now(),
                    state=DelayReportState.ASSIGNED_TO_VENDOR

                )
                if is_assigned:
                    order_report = OrderDelayReport.objects.filter(
                        agent_id=agent_id,
                        state=DelayReportState.ASSIGNED_TO_VENDOR
                    ).first()
                    message = "Assigned successfully!"
                    code = 1
                    order_report = OrderDelayReportSerializer(order_report).data
                    status = HTTP_200_OK

                    # Here, we are faced with one of the following scenarios:
                    #   1- agent_id not exists
                    #   2- agent already has assigned delay report
                    #   3- there is not any delay report in WAITING_FOR_AGENT state.
                    # We are going to return status code for each  scenario

                # 3 => there is not any delay report in WAITING_FOR_AGENT state.
                elif not OrderDelayReport.objects.filter(state=DelayReportState.WAITING_FOR_AGENT).exists():
                    message = "There is not any delay report!"
                    code = 4
                    order_report = None
                    status = HTTP_404_NOT_FOUND

                else:
                    message = "Unhandled situation!"
                    code = 5
                    order_report = None
                    status = HTTP_500_INTERNAL_SERVER_ERROR
                    logger.error(
                        f"agent {agent_id} requested to assign a delay report but there is situation that not handled!")

            except IntegrityError as e:
                if "unique_assigned_delay_report_to_one_agent" in str(e):
                    order_report = OrderDelayReport.objects.filter(
                                agent_id=agent_id,
                                state=DelayReportState.ASSIGNED_TO_VENDOR
                        ).first()
                    message = "Agent already has an assigned delay report!"
                    code = 2
                    order_report = OrderDelayReportSerializer(order_report).data
                    status = HTTP_400_BAD_REQUEST
                else:
                    return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            data={
                "message": message,
                "code": code,
                "order_report": order_report
            },
            status=status
        )
