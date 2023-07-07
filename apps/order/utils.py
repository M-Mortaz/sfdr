import logging
from datetime import datetime, timedelta, timezone

import requests
from django.conf import settings
from khayyam import JalaliDatetime

from apps.order.exc import FailedToGetNewShipmentError
from apps.order.timezone_local import TEHRAN_OFFSET, Timezone

logger = logging.getLogger(__name__)


class TehranTimezone(Timezone):
    """
    Tehran timezone with a fixed +3:30 GMT offset.
    """

    def __init__(self):
        super(TehranTimezone, self).__init__(
            TEHRAN_OFFSET,
            "Asia/Tehran"
        )


def renew_shipment_time(order_id: int) -> int:
    """Example of API response
    {
        "status": true,
        "data": {
            "eta": 14
            }
    }
    :param order_id: related order to get fresh shipment time
    :return:
    """
    last_error = None
    for _ in range(settings.RETRY_RENEW_SHIPMENT_TIME):
        try:
            response = requests.request(
                method="get",
                url=settings.RENEW_SHIPMENT_TIME_URI,
                timeout=settings.TIMEOUT_RENEW_SHIPMENT_TIME
            )
            shipment_dict = response.json()
            if not shipment_dict.get("status"):
                continue
            if isinstance(shipment_dict.get("data"), dict) and shipment_dict["data"].get("eta"):
                return shipment_dict["data"].get("eta")
        except requests.RequestException as e:
            last_error = e
            logger.exception(e)
            continue
    if last_error:
        raise last_error from None
    raise FailedToGetNewShipmentError


def first_day_of_current_week_jalali() -> datetime:
    now_jalali = JalaliDatetime.now()
    year, week, day = now_jalali.isocalendar()
    first_day_of_week_jalali_datetime = now_jalali - timedelta(days=day - 1)
    first_day_of_week_jalali_datetime_midnight = first_day_of_week_jalali_datetime.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    first_day_of_week_gregorian: datetime = first_day_of_week_jalali_datetime_midnight.todatetime()
    first_day_of_week_gregorian_tehran_tz = first_day_of_week_gregorian.replace(tzinfo=TehranTimezone())
    first_day_of_week_gregorian_utc_tz = first_day_of_week_gregorian_tehran_tz.astimezone(tz=timezone.utc)
    return first_day_of_week_gregorian_utc_tz
