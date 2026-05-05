from typing import Optional


class CreateH2hInvoiceDto:
    """DTO for creating an H2H (host-to-host) invoice."""

    def __init__(self, amount: float, order_id: str, cvv: int, month: int, year: int,
                 card_number: str, hook_url: Optional[str] = None,
                 custom_fields: Optional[str] = None, comment: Optional[str] = None,
                 success_url: Optional[str] = None, fail_url: Optional[str] = None,
                 expire: Optional[int] = 300):
        self._amount = amount
        self._order_id = order_id
        self._cvv = cvv
        self._month = month
        self._year = year
        self._card_number = card_number
        self._hook_url = hook_url
        self._custom_fields = custom_fields
        self._comment = comment
        self._success_url = success_url
        self._fail_url = fail_url
        self._expire = expire

    def get_amount(self) -> float: return self._amount
    def get_order_id(self) -> str: return self._order_id
    def get_cvv(self) -> int: return self._cvv
    def get_month(self) -> int: return self._month
    def get_year(self) -> int: return self._year
    def get_card_number(self) -> str: return self._card_number
    def get_hook_url(self) -> Optional[str]: return self._hook_url
    def get_custom_fields(self) -> Optional[str]: return self._custom_fields
    def get_comment(self) -> Optional[str]: return self._comment
    def get_success_url(self) -> Optional[str]: return self._success_url
    def get_fail_url(self) -> Optional[str]: return self._fail_url
    def get_expire(self) -> Optional[int]: return self._expire
