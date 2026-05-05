from typing import Any, Dict

from lava_sdk.dto.request.refund.get_status_refund_dto import GetStatusRefundDto
from lava_sdk.dto.response.refund.status_refund_dto import StatusRefundDto
from lava_sdk.exceptions.base_exception import LavaBaseException


class GetRefundStatus:
    def to_array(self, status_refund_dto: GetStatusRefundDto, shop_id: str) -> Dict[str, Any]:
        return {"shopId": shop_id, "refundId": status_refund_dto.get_refund_id()}

    def response_to_dto(self, refund_status: Dict[str, Any]) -> StatusRefundDto:
        if not refund_status.get("data"):
            raise LavaBaseException("Empty data")
        data = refund_status["data"]
        return StatusRefundDto(
            status=data["status"],
            refund_id=data["refund_id"],
            amount=data["amount"],
        )
