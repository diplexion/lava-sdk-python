class CreatedInvoiceDto:
    """Response DTO for a created invoice."""

    def __init__(self, invoice_id: str, amount: float, expired: str,
                 status: int, shop_id: str, url: str):
        self._invoice_id = invoice_id
        self._amount = amount
        self._expired = expired
        self._status = status
        self._shop_id = shop_id
        self._url = url

    def get_invoice_id(self) -> str: return self._invoice_id
    def get_amount(self) -> float: return self._amount
    def get_expired(self) -> str: return self._expired
    def get_status(self) -> int: return self._status
    def get_shop_id(self) -> str: return self._shop_id
    def get_url(self) -> str: return self._url
