from typing import Any, Dict

from lava_sdk.dto.request.payoff.check_wallet_request_dto import CheckWalletRequestDto
from lava_sdk.dto.response.payoff.check_wallet_response_dto import CheckWalletResponseDto
from lava_sdk.exceptions.base_exception import LavaBaseException


class CheckWalletDto:
    def to_array(self, payoff_dto: CheckWalletRequestDto, profile_id: str) -> Dict[str, Any]:
        return {
            "profileId": profile_id,
            "service": payoff_dto.get_service(),
            "walletTo": payoff_dto.get_wallet(),
        }

    def to_dto(self, response: Dict[str, Any]) -> CheckWalletResponseDto:
        if not response.get("data"):
            raise LavaBaseException("Empty data")
        return CheckWalletResponseDto(status=response["data"]["status"])
