class ShopBalanceDto:
    """Response DTO for shop balance."""

    def __init__(self, balance: float, freeze_balance: float):
        self._balance = balance
        self._freeze_balance = freeze_balance

    def get_balance(self) -> float: return self._balance
    def get_freeze_balance(self) -> float: return self._freeze_balance
