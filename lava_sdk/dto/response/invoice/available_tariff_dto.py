class AvailableTariffDto:
    """Response DTO for an available invoice tariff."""

    def __init__(self, status: int, percent: float, user_percent: float,
                 shop_percent: float, service_name: str, service_id: str, currency: str):
        self._status = status
        self._percent = percent
        self._user_percent = user_percent
        self._shop_percent = shop_percent
        self._service_name = service_name
        self._service_id = service_id
        self._currency = currency

    def get_percent(self) -> float: return self._percent
    def set_percent(self, v: float) -> None: self._percent = v
    def get_user_percent(self) -> float: return self._user_percent
    def set_user_percent(self, v: float) -> None: self._user_percent = v
    def get_shop_percent(self) -> float: return self._shop_percent
    def set_shop_percent(self, v: float) -> None: self._shop_percent = v
    def get_service_name(self) -> str: return self._service_name
    def set_service_name(self, v: str) -> None: self._service_name = v
    def get_service_id(self) -> str: return self._service_id
    def set_service_id(self, v: str) -> None: self._service_id = v
    def get_status(self) -> int: return self._status
    def set_status(self, v: int) -> None: self._status = v
    def get_currency(self) -> str: return self._currency
    def set_currency(self, v: str) -> None: self._currency = v
