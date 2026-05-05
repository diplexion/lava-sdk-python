import hashlib
import hmac
import json


class ClientGenerateSignature:
    """Generates HMAC-SHA256 signatures for API requests."""

    def __init__(self, secret_key: str):
        self._secret_key = secret_key

    def generate_signature(self, data: dict) -> str:
        """
        Generate HMAC-SHA256 signature.

        Keys are sorted alphabetically (equivalent to PHP ksort),
        then JSON-encoded without spaces, then HMAC-SHA256 signed.
        """
        sorted_data = dict(sorted(data.items()))
        payload = json.dumps(sorted_data, separators=(",", ":"), ensure_ascii=True)
        return hmac.new(
            self._secret_key.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
