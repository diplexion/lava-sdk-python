from typing import Any, Dict

from lava_sdk.dto.response.profile.profile_balance_dto import ProfileBalanceDto
from lava_sdk.exceptions.base_exception import LavaBaseException


class GetProfileBalance:
    def to_array(self, profile_id: str) -> Dict[str, Any]:
        return {"profileId": profile_id}

    def to_dto(self, response: Dict[str, Any]) -> ProfileBalanceDto:
        if not response.get("data"):
            raise LavaBaseException("Empty data")
        data = response["data"]
        return ProfileBalanceDto(
            total_balance=data["balance"],
            available_balance=data["active_balance"],
            freeze_balance=data["freeze_balance"],
        )
