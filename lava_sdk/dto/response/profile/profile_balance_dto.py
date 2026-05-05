class ProfileBalanceDto:
    """Response DTO for profile balance."""

    def __init__(self, total_balance: float, available_balance: float, freeze_balance: float):
        self._total_balance = total_balance
        self._available_balance = available_balance
        self._freeze_balance = freeze_balance

    def get_total_balance(self) -> float: return self._total_balance
    def get_available_balance(self) -> float: return self._available_balance
    def get_freeze_balance(self) -> float: return self._freeze_balance
