import hashlib
import hmac
import json
from typing import Optional


class ClientCheckSignatureWebhook:
    """Verifies HMAC-SHA256 signatures on incoming webhooks."""

    def __init__(self, secret_key: Optional[str]):
        self._secret_key = secret_key

    def check_sign_webhook(self, webhook_response: str, signature: str) -> bool:
        """
        Verify an incoming webhook signature.

        :param webhook_response: Raw JSON string from the webhook body
        :param signature: Expected HMAC-SHA256 signature
        :return: True if the computed signature matches
        """
        data = json.loads(webhook_response)
        sorted_data = dict(sorted(data.items()))
        payload = json.dumps(sorted_data, separators=(",", ":"), ensure_ascii=True)
        computed = hmac.new(
            self._secret_key.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return computed == signature
