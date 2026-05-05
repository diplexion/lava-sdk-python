from typing import Optional


class GetStatusInvoiceDto:
    """DTO for checking invoice status."""

    def __init__(self, order_id: Optional[str] = None, invoice_id: Optional[str] = None):
        self._order_id = order_id
        self._invoice_id = invoice_id

    def get_order_id(self) -> Optional[str]: return self._order_id
    def get_invoice_id(self) -> Optional[str]: return self._invoice_id
