import hashlib
import hmac
import json
import uuid

from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto
from lava_sdk.http.lava_facade import LavaFacade


def test_webhook_signature_valid():
    additional_key = "f4b91efb9b8da35737fcd97ab123c74566f9a654"
    signature = "b0b011552beb994cc04401e088db7b296796a07fc76976b632518fe146ffa330"
    data = {
        "invoice_id": "18cf0c0b-6539-4d7c-b3e9-479e4922b87c",
        "status": "success",
        "pay_time": "2022-11-08 11:26:46",
        "amount": "1.00",
        "order_id": "636a3c2f3e82b",
        "pay_service": "card",
        "payer_details": "553691******8079",
        "custom_fields": "test",
        "type": 1,
        "credited": "1.00",
    }
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), additional_key=additional_key)
    assert facade.check_sign_webhook(json.dumps(data), signature) is True


def _generate_sign(data: dict, secret: str) -> str:
    sorted_data = dict(sorted(data.items()))
    payload = json.dumps(sorted_data, separators=(",", ":"), ensure_ascii=True)
    return hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()


def test_payoff_webhook_success():
    profile_additional_key = str(uuid.uuid4())
    profile_data = ProfileSecretDto(
        str(uuid.uuid4()), str(uuid.uuid4()), profile_additional_key
    )
    data = {
        "payoff_id": str(uuid.uuid4()),
        "status": "success",
        "payoff_time": "2026-03-16 12:01:43",
        "payoff_service": "card",
        "type": 3,
        "credited": "10000.00",
        "order_id": str(uuid.uuid4()),
    }
    signature = _generate_sign(data, profile_additional_key)
    facade = LavaFacade(
        str(uuid.uuid4()), str(uuid.uuid4()),
        str(uuid.uuid4()), profile_secret_data=profile_data
    )
    assert facade.check_payoff_signature(json.dumps(data), signature) is True
