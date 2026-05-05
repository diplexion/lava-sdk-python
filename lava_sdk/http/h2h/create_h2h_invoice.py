from typing import Any, Dict

from lava_sdk.dto.request.h2h.create_h2h_invoice_dto import CreateH2hInvoiceDto
from lava_sdk.dto.response.h2h.created_h2h_invoice_dto import CreatedH2hInvoiceDto
from lava_sdk.exceptions.base_exception import LavaBaseException


class CreateH2hInvoice:
    def to_array(self, h2h_dto: CreateH2hInvoiceDto, shop_id: str) -> Dict[str, Any]:
        return {
            "sum": h2h_dto.get_amount(),
            "orderId": h2h_dto.get_order_id(),
            "hookUrl": h2h_dto.get_hook_url(),
            "expire": h2h_dto.get_expire(),
            "customFields": h2h_dto.get_custom_fields(),
            "comment": h2h_dto.get_comment(),
            "shopId": shop_id,
            "cardNumber": h2h_dto.get_card_number(),
            "cvv": h2h_dto.get_cvv(),
            "month": h2h_dto.get_month(),
            "year": h2h_dto.get_year(),
            "successUrl": h2h_dto.get_success_url(),
            "failUrl": h2h_dto.get_fail_url(),
        }

    def to_dto(self, response: Dict[str, Any]) -> CreatedH2hInvoiceDto:
        if not response.get("data"):
            raise LavaBaseException("Empty data")
        data = response["data"]
        return CreatedH2hInvoiceDto(
            url=data["url"],
            invoice_id=data["invoiceId"],
            card_mask=data["cardMask"],
            amount=data["amount"],
            amount_pay=data["amountPay"],
            commission=data["commission"],
            shop_id=data["shopId"],
        )
