from typing import Any, Dict

from lava_sdk.dto.request.invoice.get_status_invoice_dto import GetStatusInvoiceDto
from lava_sdk.dto.response.invoice.status_invoice_dto import StatusInvoiceDto
from lava_sdk.exceptions.base_exception import LavaBaseException


class GetStatusInvoice:
    def to_array(self, invoice_dto: GetStatusInvoiceDto, shop_id: str) -> Dict[str, Any]:
        return {
            "shopId": shop_id,
            "orderId": invoice_dto.get_order_id(),
            "invoiceId": invoice_dto.get_invoice_id(),
        }

    def to_dto(self, invoice: Dict[str, Any]) -> StatusInvoiceDto:
        if not invoice.get("data"):
            raise LavaBaseException("Empty data")
        data = invoice["data"]
        return StatusInvoiceDto(
            status=data["status"],
            error_message=data.get("error_message"),
            invoice_id=data["id"],
            shop_id=data["shop_id"],
            amount=data["amount"],
            expire=data["expire"],
            order_id=data["order_id"],
            fail_url=data.get("fail_url"),
            success_url=data.get("success_url"),
            hook_url=data.get("hook_url"),
            custom_fields=data.get("custom_fields"),
            include_service=data.get("include_service"),
            exclude_service=data.get("exclude_service"),
        )
