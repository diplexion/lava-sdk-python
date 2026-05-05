class CreatedPayoffDto:
    """Response DTO for a created payoff."""

    def __init__(self, payoff_id: str, status: str):
        self._payoff_id = payoff_id
        self._status = status

    def get_payoff_id(self) -> str: return self._payoff_id
    def get_status(self) -> str: return self._status
