class CurrencyDto:
    """Represents a currency."""

    def __init__(self, label: str, symbol: str, value: str):
        self.label = label
        self.symbol = symbol
        self.value = value

    def get_label(self) -> str: return self.label
    def get_symbol(self) -> str: return self.symbol
    def get_value(self) -> str: return self.value
