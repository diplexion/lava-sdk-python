from typing import Any, Dict

from lava_sdk.dto.request.payoff.get_payoff_status_dto import GetPayoffStatusDto
from lava_sdk.dto.response.payoff.status_payoff_dto import StatusPayoffDto
from lava_sdk.exceptions.base_exception import LavaBaseException


class GetStatusPayoff:
    def to_array(self, get_payoff_status: GetPayoffStatusDto, profile_id: str) -> Dict[str, Any]:
        return {
            "shopId": profile_id,
            "orderId": get_payoff_status.get_order_id(),
            "payoffId": get_payoff_status.get_payoff_id(),
        }

    def to_dto(self, data: Dict[str, Any]) -> StatusPayoffDto:
        if not data.get("data"):
            raise LavaBaseException("Data is empty")
        d = data["data"]
        return StatusPayoffDto(
            id=d["id"],
            order_id=d["orderId"],
            status=d["status"],
            wallet=d.get("wallet"),
            service=d["service"],
            amount_pay=d["amountPay"],
            commission=d["commission"],
            amount_receive=d["amountReceive"],
            try_count=d["tryCount"],
            error_message=d.get("errorMessage"),
        )
