class CheckWalletResponseDto:
    """Response DTO for wallet check."""

    def __init__(self, status: bool):
        self._status = status

    def get_status(self) -> bool: return self._status
