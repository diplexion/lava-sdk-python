class CreatedRefundDto:
    """Response DTO for a created refund."""

    def __init__(self, status: str, refund_id: str, amount: float, service: str, label: str):
        self._status = status
        self._refund_id = refund_id
        self._amount = amount
        self._service = service
        self._label = label

    def get_status(self) -> str: return self._status
    def get_refund_id(self) -> str: return self._refund_id
    def get_amount(self) -> float: return self._amount
    def get_service(self) -> str: return self._service
    def get_label(self) -> str: return self._label
