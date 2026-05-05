import json
from typing import Any, Dict

from lava_sdk.constants.course_url_constants import CourseUrlConstants
from lava_sdk.constants.h2h_url_constants import H2hUrlConstants
from lava_sdk.constants.invoice_url_constants import InvoiceUrlConstants
from lava_sdk.constants.payoff_url_constants import PayoffUrlConstants
from lava_sdk.constants.profile_url_constants import ProfileUrlConstants
from lava_sdk.constants.refund_url_constants import RefundUrlConstants
from lava_sdk.constants.shop_url_constants import ShopUrlConstants
from lava_sdk.exceptions.course.course_exception import CourseException
from lava_sdk.exceptions.h2h.h2h_exception import H2hException
from lava_sdk.exceptions.invoice.invoice_exception import InvoiceException
from lava_sdk.exceptions.payoff.check_wallet_exception import CheckWalletException
from lava_sdk.exceptions.payoff.error_get_payoff_tariff_exception import ErrorGetPayoffTariffException
from lava_sdk.exceptions.payoff.payoff_exception import PayoffException
from lava_sdk.exceptions.profile.profile_exception import ProfileException
from lava_sdk.exceptions.refund.refund_exception import RefundException
from lava_sdk.exceptions.shop.shop_exception import ShopException
from lava_sdk.http.client.http_client import HttpClient


def _err(error: Any) -> str:
    """Serialize error to string (mirrors PHP behavior for array errors)."""
    if isinstance(error, (dict, list)):
        return json.dumps(error, ensure_ascii=False)
    return str(error) if error is not None else ""


class Client:
    """HTTP client for all Lava API endpoints."""

    def __init__(self):
        self._http_client = HttpClient()

    def set_http_client(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def create_refund(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self._http_client.post_request(RefundUrlConstants.CREATE_REFUND, data)
        if response.get("error") or response.get("status") != 200:
            raise RefundException(_err(response.get("error")), response.get("status", 0))
        return response

    def get_refund_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self._http_client.post_request(RefundUrlConstants.GET_STATUS_REFUND, data)
        if response.get("error") or response.get("status") != 200:
            raise RefundException(_err(response.get("error")), response.get("status", 0))
        return response

    def get_shop_balance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self._http_client.post_request(ShopUrlConstants.GET_BALANCE, data)
        if response.get("error") or response.get("status") != 200:
            raise ShopException(_err(response.get("error")), response.get("status", 0))
        return response

    def create_invoice(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self._http_client.post_request(InvoiceUrlConstants.INVOICE_CREATE, data)
        if response.get("error") or response.get("status") != 200:
            raise InvoiceException(_err(response.get("error")), response.get("status", 0))
        return response

    def get_invoice_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not data.get("orderId") and not data.get("invoiceId"):
            raise InvoiceException("orderId or invoiceId required", 422)
        response = self._http_client.post_request(InvoiceUrlConstants.INVOICE_STATUS, data)
        if response.get("error") or response.get("status") != 200:
            raise InvoiceException(_err(response.get("error")), response.get("status", 0))
        return response

    def create_payoff(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self._http_client.post_request(PayoffUrlConstants.CREATE_PAYOFF, data)
        if response.get("error") or response.get("status") != 200:
            raise PayoffException(_err(response.get("error")), response.get("status", 0))
        return response

    def get_payoff_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not data.get("orderId") and not data.get("payoffId"):
            raise PayoffException("orderId or payoffId required", 422)
        response = self._http_client.post_request(PayoffUrlConstants.GET_PAYOFF_STATUS, data)
        if response.get("error") or response.get("status") != 200:
            raise PayoffException(_err(response.get("error")), response.get("status", 0))
        return response

    def create_h2h_invoice(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self._http_client.post_request(H2hUrlConstants.INVOICE_CREATE, data)
        if response.get("error") or response.get("status") != 200:
            raise H2hException(_err(response.get("error")), response.get("status", 0))
        return response

    def create_h2h_sbp(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self._http_client.post_request(H2hUrlConstants.SBP_INVOICE_CREATE, data)
        if response.get("error") or response.get("status") != 200:
            raise H2hException(_err(response.get("error")), response.get("status", 0))
        return response

    def check_wallet(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self._http_client.post_request(PayoffUrlConstants.CHECK_USER_WALLET, data, timeout=35)
        if response.get("error") or response.get("status") != 200:
            raise CheckWalletException(_err(response.get("error")), response.get("status", 0))
        return response

    def get_payoff_tariffs(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self._http_client.post_request(PayoffUrlConstants.GET_PAYOFF_TARIFFS, data)
        tariffs_ok = isinstance(response.get("data"), dict) and response["data"].get("tariffs")
        if response.get("error") or response.get("status") != 200 or not tariffs_ok:
            raise ErrorGetPayoffTariffException(_err(response.get("error")), response.get("status", 0))
        return response

    def get_availible_tariffs(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self._http_client.post_request(InvoiceUrlConstants.GET_AVAILIBLE_TARIFFS, data)
        if response.get("error") or response.get("status") != 200:
            raise InvoiceException(_err(response.get("error")), response.get("status", 0))
        return response

    def get_profile_balance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self._http_client.get_request(ProfileUrlConstants.GET_BALANCE, data)
        if response.get("error") or response.get("status") != 200:
            raise ProfileException(_err(response.get("error")), response.get("status", 0))
        return response

    def get_payment_course_list(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self._http_client.get_request(CourseUrlConstants.GET_PAYMENT_COURSE_LIST, data)
        if response.get("error") or response.get("status") != 200:
            raise CourseException(_err(response.get("error")), response.get("status", 0))
        return response

    def get_payoff_course_list(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self._http_client.get_request(CourseUrlConstants.GET_PAYOFF_COURSE_LIST, data)
        if response.get("error") or response.get("status") != 200:
            raise CourseException(_err(response.get("error")), response.get("status", 0))
        return response
