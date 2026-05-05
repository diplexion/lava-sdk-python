from typing import Optional


class StatusPayoffDto:
    """Response DTO for payoff status."""

    def __init__(self, id: str, order_id: str, status: str, wallet: Optional[str],
                 service: str, amount_pay: float, commission: float,
                 amount_receive: float, try_count: int, error_message: Optional[str]):
        self._id = id
        self._order_id = order_id
        self._status = status
        self._wallet = wallet
        self._service = service
        self._amount_pay = amount_pay
        self._commission = commission
        self._amount_receive = amount_receive
        self._try_count = try_count
        self._error_message = error_message

    def get_id(self) -> str: return self._id
    def get_order_id(self) -> str: return self._order_id
    def get_status(self) -> str: return self._status
    def get_service(self) -> str: return self._service
    def get_amount_pay(self) -> float: return self._amount_pay
    def get_commission(self) -> float: return self._commission
    def get_amount_receive(self) -> float: return self._amount_receive
    def get_try_count(self) -> int: return self._try_count
    def get_wallet(self) -> Optional[str]: return self._wallet
    def get_error_message(self) -> Optional[str]: return self._error_message
