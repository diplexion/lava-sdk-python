from typing import Any, Dict

from lava_sdk.dto.request.invoice.create_invoice_dto import CreateInvoiceDto
from lava_sdk.dto.response.invoice.created_invoice_dto import CreatedInvoiceDto
from lava_sdk.exceptions.base_exception import LavaBaseException


class CreateInvoice:
    def to_array(self, invoice_dto: CreateInvoiceDto, shop_id: str) -> Dict[str, Any]:
        return {
            "sum": invoice_dto.get_sum(),
            "orderId": invoice_dto.get_order_id(),
            "hookUrl": invoice_dto.get_hook_url(),
            "failUrl": invoice_dto.get_fail_url(),
            "successUrl": invoice_dto.get_success_url(),
            "expire": invoice_dto.get_expire(),
            "customFields": invoice_dto.get_custom_fields(),
            "comment": invoice_dto.get_comment(),
            "includeService": invoice_dto.get_include_service(),
            "excludeService": invoice_dto.get_exclude_service(),
            "shopId": shop_id,
        }

    def to_dto(self, invoice: Dict[str, Any]) -> CreatedInvoiceDto:
        if not invoice.get("data"):
            raise LavaBaseException("Empty data")
        data = invoice["data"]
        return CreatedInvoiceDto(
            invoice_id=data["id"],
            amount=data["amount"],
            expired=data["expired"],
            status=data["status"],
            shop_id=data["shop_id"],
            url=data["url"],
        )
