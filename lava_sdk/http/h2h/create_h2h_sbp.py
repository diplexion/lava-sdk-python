from typing import Any, Dict

from lava_sdk.dto.request.h2h.create_sbp_h2h_dto import CreateSBPH2HDto
from lava_sdk.dto.response.h2h.created_sbp_h2h_dto import CreatedSBPH2hDto
from lava_sdk.exceptions.base_exception import LavaBaseException


class CreateH2HSbp:
    def to_array(self, h2h_dto: CreateSBPH2HDto, shop_id: str) -> Dict[str, Any]:
        return {
            "sum": h2h_dto.get_amount(),
            "orderId": h2h_dto.get_order_id(),
            "hookUrl": h2h_dto.get_hook_url(),
            "expire": h2h_dto.get_expire(),
            "customFields": h2h_dto.get_custom_fields(),
            "comment": h2h_dto.get_comment(),
            "shopId": shop_id,
            "ip": h2h_dto.get_ip(),
            "successUrl": h2h_dto.get_success_url(),
            "failUrl": h2h_dto.get_fail_url(),
        }

    def to_dto(self, invoice: Dict[str, Any]) -> CreatedSBPH2hDto:
        if not invoice.get("data"):
            raise LavaBaseException("Empty data")
        data = invoice["data"]
        return CreatedSBPH2hDto(
            sbp_url=data["sbp_url"],
            fingerprint=data["fingerprint"],
            qr_code=data["qr_code"],
        )
