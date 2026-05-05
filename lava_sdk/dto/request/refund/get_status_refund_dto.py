class GetStatusRefundDto:
    """DTO for checking refund status."""

    def __init__(self, refund_id: str):
        self._refund_id = refund_id

    def get_refund_id(self) -> str: return self._refund_id
