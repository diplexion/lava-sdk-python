class CreatedH2hInvoiceDto:
    """Response DTO for a created H2H invoice."""

    def __init__(self, url: str, invoice_id: str, card_mask: str,
                 amount: float, amount_pay: float, commission: float, shop_id: str):
        self._url = url
        self._invoice_id = invoice_id
        self._card_mask = card_mask
        self._amount = amount
        self._amount_pay = amount_pay
        self._commission = commission
        self._shop_id = shop_id

    def get_url(self) -> str: return self._url
    def get_invoice_id(self) -> str: return self._invoice_id
    def get_card_mask(self) -> str: return self._card_mask
    def get_amount(self) -> float: return self._amount
    def get_amount_pay(self) -> float: return self._amount_pay
    def get_commission(self) -> float: return self._commission
    def get_shop_id(self) -> str: return self._shop_id
