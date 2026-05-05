class LavaBaseException(Exception):
    """Base exception for all Lava SDK exceptions."""

    def __init__(self, message: str = "", code: int = 0):
        super().__init__(message)
        self.code = code
