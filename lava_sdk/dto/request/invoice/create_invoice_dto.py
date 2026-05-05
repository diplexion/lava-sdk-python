from typing import List, Optional


class CreateInvoiceDto:
    """DTO for creating a payment invoice."""

    def __init__(self, sum: str, order_id: str, hook_url: Optional[str] = None,
                 success_url: Optional[str] = None, fail_url: Optional[str] = None,
                 expire: Optional[int] = None, custom_fields: Optional[str] = None,
                 comment: Optional[str] = None, exclude_service: Optional[List[str]] = None,
                 include_service: Optional[List[str]] = None):
        self._sum = sum
        self._order_id = order_id
        self._hook_url = hook_url
        self._success_url = success_url
        self._fail_url = fail_url
        self._expire = expire
        self._custom_fields = custom_fields
        self._comment = comment
        self._exclude_service = exclude_service
        self._include_service = include_service

    def get_sum(self) -> str: return self._sum
    def get_order_id(self) -> str: return self._order_id
    def get_hook_url(self) -> Optional[str]: return self._hook_url
    def get_success_url(self) -> Optional[str]: return self._success_url
    def get_fail_url(self) -> Optional[str]: return self._fail_url
    def get_expire(self) -> Optional[int]: return self._expire
    def get_custom_fields(self) -> Optional[str]: return self._custom_fields
    def get_comment(self) -> Optional[str]: return self._comment
    def get_include_service(self) -> Optional[List[str]]: return self._include_service
    def get_exclude_service(self) -> Optional[List[str]]: return self._exclude_service
