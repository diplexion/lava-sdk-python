class CheckWalletRequestDto:
    """DTO for checking wallet validity."""

    def __init__(self, service: str, wallet_to: str):
        self._service = service
        self._wallet_to = wallet_to

    def get_service(self) -> str: return self._service
    def get_wallet(self) -> str: return self._wallet_to
