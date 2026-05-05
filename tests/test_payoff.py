import uuid
import pytest

from lava_sdk.dto.request.payoff.check_wallet_request_dto import CheckWalletRequestDto
from lava_sdk.dto.request.payoff.create_payoff_dto import CreatePayoffDto
from lava_sdk.dto.request.payoff.get_payoff_status_dto import GetPayoffStatusDto
from lava_sdk.dto.response.payoff.check_wallet_response_dto import CheckWalletResponseDto
from lava_sdk.dto.response.payoff.created_payoff_dto import CreatedPayoffDto
from lava_sdk.dto.response.payoff.status_payoff_dto import StatusPayoffDto
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto
from lava_sdk.exceptions.payoff.check_wallet_exception import CheckWalletException
from lava_sdk.exceptions.payoff.payoff_exception import PayoffException
from lava_sdk.http.lava_facade import LavaFacade
from tests.Mocks.client_error_response_mock import ClientErrorResponseMock
from tests.Mocks.client_success_response_mock import ClientSuccessResponseMock


def _facade(client):
    profile = ProfileSecretDto(str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()))
    return LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=client, profile_secret_data=profile)


def test_create_payoff_success():
    response = _facade(ClientSuccessResponseMock()).create_payoff(
        CreatePayoffDto(str(uuid.uuid4()), 10, "lava_payoff")
    )
    assert isinstance(response, CreatedPayoffDto)


def test_create_payoff_fail():
    with pytest.raises(PayoffException) as exc_info:
        _facade(ClientErrorResponseMock()).create_payoff(
            CreatePayoffDto(str(uuid.uuid4()), 10, "lava_payoff")
        )
    assert exc_info.value.args[0] == "Insufficient balance in shop"


def test_get_status_payoff_success():
    response = _facade(ClientSuccessResponseMock()).get_status_payoff(
        GetPayoffStatusDto(payoff_id=str(uuid.uuid4()))
    )
    assert isinstance(response, StatusPayoffDto)


def test_get_status_payoff_fail():
    with pytest.raises(PayoffException) as exc_info:
        _facade(ClientErrorResponseMock()).get_status_payoff(
            GetPayoffStatusDto(payoff_id=str(uuid.uuid4()))
        )
    assert exc_info.value.args[0] == "Payoff not found"


def test_check_wallet_success():
    response = _facade(ClientSuccessResponseMock()).check_wallet(
        CheckWalletRequestDto("steam_payoff", str(uuid.uuid4()))
    )
    assert isinstance(response, CheckWalletResponseDto)


def test_check_wallet_fail():
    import json
    with pytest.raises(CheckWalletException) as exc_info:
        _facade(ClientErrorResponseMock()).check_wallet(
            CheckWalletRequestDto("steam_payoff", str(uuid.uuid4()))
        )
    assert exc_info.value.args[0] == json.dumps({"walletTo": ["Account not found"]})
