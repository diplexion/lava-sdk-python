from lava_sdk.dto.response.course.currency_dto import CurrencyDto


class CourseDto:
    """Represents a currency exchange rate."""

    def __init__(self, currency: CurrencyDto, value: float):
        self._currency = currency
        self._value = value

    def get_currency(self) -> CurrencyDto: return self._currency
    def get_value(self) -> float: return self._value
