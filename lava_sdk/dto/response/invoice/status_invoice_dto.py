from typing import List, Optional


class StatusInvoiceDto:
    """Response DTO for invoice status."""

    def __init__(self, status: str, error_message: Optional[str], invoice_id: str,
                 shop_id: str, amount: float, expire: str, order_id: str,
                 fail_url: Optional[str], success_url: Optional[str],
                 hook_url: Optional[str], custom_fields: Optional[str],
                 include_service: Optional[List[str]], exclude_service: Optional[List[str]]):
        self._status = status
        self._error_message = error_message
        self._invoice_id = invoice_id
        self._shop_id = shop_id
        self._amount = amount
        self._expire = expire
        self._order_id = order_id
        self._fail_url = fail_url
        self._success_url = success_url
        self._hook_url = hook_url
        self._custom_fields = custom_fields
        self._include_service = include_service
        self._exclude_service = exclude_service

    def get_status(self) -> str: return self._status
    def get_error_message(self) -> Optional[str]: return self._error_message
    def get_invoice_id(self) -> str: return self._invoice_id
    def get_shop_id(self) -> str: return self._shop_id
    def get_amount(self) -> float: return self._amount
    def get_expire(self) -> str: return self._expire
    def get_order_id(self) -> str: return self._order_id
    def get_fail_url(self) -> Optional[str]: return self._fail_url
    def get_success_url(self) -> Optional[str]: return self._success_url
    def get_hook_url(self) -> Optional[str]: return self._hook_url
    def get_custom_fields(self) -> Optional[str]: return self._custom_fields
    def get_include_service(self) -> Optional[List[str]]: return self._include_service
    def get_exclude_service(self) -> Optional[List[str]]: return self._exclude_service
