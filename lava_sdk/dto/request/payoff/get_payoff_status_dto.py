from typing import Optional


class GetPayoffStatusDto:
    """DTO for checking payoff status."""

    def __init__(self, order_id: Optional[str] = None, payoff_id: Optional[str] = None):
        self._order_id = order_id
        self._payoff_id = payoff_id

    def get_order_id(self) -> Optional[str]: return self._order_id
    def get_payoff_id(self) -> Optional[str]: return self._payoff_id
