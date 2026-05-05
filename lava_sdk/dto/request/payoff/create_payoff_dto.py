from typing import Optional


class CreatePayoffDto:
    """DTO for creating a payoff (payout)."""

    def __init__(self, order_id: str, amount: float, service: str,
                 subtract: Optional[int] = None, wallet_to: Optional[str] = None,
                 hook_url: Optional[str] = None):
        self._order_id = order_id
        self._amount = amount
        self._service = service
        self._subtract = subtract
        self._wallet_to = wallet_to
        self._hook_url = hook_url

    def get_order_id(self) -> str: return self._order_id
    def get_amount(self) -> float: return self._amount
    def get_service(self) -> str: return self._service
    def get_subtract(self) -> Optional[int]: return self._subtract
    def get_wallet_to(self) -> Optional[str]: return self._wallet_to
    def get_hook_url(self) -> Optional[str]: return self._hook_url
