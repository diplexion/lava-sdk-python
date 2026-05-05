from typing import Any, Dict

from lava_sdk.dto.request.payoff.create_payoff_dto import CreatePayoffDto
from lava_sdk.dto.response.payoff.created_payoff_dto import CreatedPayoffDto
from lava_sdk.exceptions.base_exception import LavaBaseException


class CreatePayoff:
    def to_array(self, payoff_dto: CreatePayoffDto, profile_id: str) -> Dict[str, Any]:
        return {
            "profileId": profile_id,
            "amount": payoff_dto.get_amount(),
            "service": payoff_dto.get_service(),
            "walletTo": payoff_dto.get_wallet_to(),
            "subtract": payoff_dto.get_subtract(),
            "hookUrl": payoff_dto.get_hook_url(),
            "orderId": payoff_dto.get_order_id(),
        }

    def to_dto(self, response: Dict[str, Any]) -> CreatedPayoffDto:
        if not response.get("data"):
            raise LavaBaseException("Empty data")
        data = response["data"]
        return CreatedPayoffDto(payoff_id=data["payoff_id"], status=data["payoff_status"])
