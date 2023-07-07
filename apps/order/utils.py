import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class FailedToGetNewShipmentError(Exception):
    pass


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
