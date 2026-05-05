from typing import Any, Dict

from lava_sdk.dto.response.shop.shop_balance_dto import ShopBalanceDto
from lava_sdk.exceptions.base_exception import LavaBaseException


class GetShopBalance:
    def to_array(self, shop_id: str) -> Dict[str, Any]:
        return {"shopId": shop_id}

    def to_dto(self, response: Dict[str, Any]) -> ShopBalanceDto:
        if not response.get("data"):
            raise LavaBaseException("Empty data")
        data = response["data"]
        return ShopBalanceDto(balance=data["balance"], freeze_balance=data["freeze_balance"])
