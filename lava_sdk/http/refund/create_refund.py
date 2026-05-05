from typing import Any, Dict

from lava_sdk.dto.request.refund.create_refund_dto import CreateRefundDto
from lava_sdk.dto.response.refund.created_refund_dto import CreatedRefundDto
from lava_sdk.exceptions.base_exception import LavaBaseException


class CreateRefund:
    def to_array(self, refund_dto: CreateRefundDto, shop_id: str) -> Dict[str, Any]:
        return {
            "shopId": shop_id,
            "invoiceId": refund_dto.get_invoice_id(),
            "amount": refund_dto.get_amount(),
            "description": refund_dto.get_description(),
        }

    def to_dto(self, refund: Dict[str, Any]) -> CreatedRefundDto:
        if not refund.get("data"):
            raise LavaBaseException(refund.get("error", "Empty data"))
        data = refund["data"]
        return CreatedRefundDto(
            status=data["status"],
            refund_id=data["refund_id"],
            amount=data["amount"],
            service=data["service"],
            label=data["label"],
        )
