from typing import Optional


class CreateRefundDto:
    """DTO for creating a refund."""

    def __init__(self, invoice_id: str, description: Optional[str] = None,
                 amount: Optional[float] = None):
        self._invoice_id = invoice_id
        self._description = description
        self._amount = amount

    def get_invoice_id(self) -> str: return self._invoice_id
    def get_description(self) -> Optional[str]: return self._description
    def get_amount(self) -> Optional[float]: return self._amount
