from typing import Optional


class ProfileSecretDto:
    """Holds profile-level authentication credentials."""

    def __init__(self, profile_id: str, secret_key: str, additional_key: Optional[str] = None):
        self._profile_id = profile_id
        self._secret_key = secret_key
        self._additional_key = additional_key

    def get_profile_id(self) -> str:
        return self._profile_id

    def get_secret_key(self) -> str:
        return self._secret_key

    def get_additional_key(self) -> Optional[str]:
        return self._additional_key
