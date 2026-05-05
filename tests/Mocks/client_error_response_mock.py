import json
from typing import Any, Dict

from lava_sdk.exceptions.course.course_exception import CourseException
from lava_sdk.exceptions.invoice.invoice_exception import InvoiceException
from lava_sdk.exceptions.payoff.check_wallet_exception import CheckWalletException
from lava_sdk.exceptions.payoff.payoff_exception import PayoffException
from lava_sdk.exceptions.profile.profile_exception import ProfileException
from lava_sdk.exceptions.refund.refund_exception import RefundException
from lava_sdk.exceptions.shop.shop_exception import ShopException


class ClientErrorResponseMock:
    """Mock client that raises typed exceptions for all endpoints."""

    def create_refund(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise RefundException("Invoice not found", 404)

    def get_refund_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise RefundException("Refund not found", 404)

    def create_invoice(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise InvoiceException("OrderId must be uniq", 422)

    def get_invoice_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise ShopException("Invoice not found", 404)

    def get_shop_balance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise ShopException("Field shopId is required", 422)

    def create_payoff(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise PayoffException("Insufficient balance in shop", 405)

    def get_payoff_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise PayoffException("Payoff not found", 404)

    def create_h2h_invoice(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise PayoffException("Payment method was not found for this user", 405)

    def create_h2h_sbp(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise PayoffException("Payment method was not found for this user", 405)

    def check_wallet(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise CheckWalletException(json.dumps({"walletTo": ["Account not found"]}), 422)

    def get_payoff_tariffs(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {}

    def get_availible_tariffs(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise PayoffException("Profile not found", 404)

    def get_profile_balance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise ProfileException("Profile not found", 404)

    def get_payoff_course_list(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise CourseException("Unauthorized", 401)

    def get_payment_course_list(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise CourseException("Unauthorized", 401)
