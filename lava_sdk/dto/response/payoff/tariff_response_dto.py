from typing import Optional


class TariffResponseDto:
    """Response DTO for a payoff tariff."""

    def __init__(self, percent: Optional[float], max_sum: Optional[float], service: str,
                 fix: Optional[float], title: Optional[str], currency: str,
                 min_sum: Optional[float]):
        self.percent = percent
        self.max_sum = max_sum
        self.service = service
        self.fix = fix
        self.title = title
        self.currency = currency
        self.min_sum = min_sum

    def get_percent(self) -> Optional[float]: return self.percent
    def set_percent(self, v: float) -> None: self.percent = v
    def get_min_sum(self) -> Optional[float]: return self.min_sum
    def set_min_sum(self, v: Optional[float]) -> None: self.min_sum = v
    def get_max_sum(self) -> Optional[float]: return self.max_sum
    def set_max_sum(self, v: Optional[float]) -> None: self.max_sum = v
    def get_service(self) -> str: return self.service
    def set_service(self, v: str) -> None: self.service = v
    def get_fix(self) -> Optional[float]: return self.fix
    def set_fix(self, v: Optional[float]) -> None: self.fix = v
    def get_title(self) -> Optional[str]: return self.title
    def set_title(self, v: Optional[str]) -> None: self.title = v
    def get_currency(self) -> str: return self.currency
    def set_currency(self, v: str) -> None: self.currency = v
