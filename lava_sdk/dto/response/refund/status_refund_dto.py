class StatusRefundDto:
    """Response DTO for refund status."""

    def __init__(self, status: str, refund_id: str, amount: float):
        self._status = status
        self._refund_id = refund_id
        self._amount = amount

    def get_status(self) -> str: return self._status
    def get_refund_id(self) -> str: return self._refund_id
    def get_amount(self) -> float: return self._amount
