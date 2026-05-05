import uuid
import pytest

from lava_sdk.dto.response.profile.profile_balance_dto import ProfileBalanceDto
from lava_sdk.dto.secret.profile_secret_dto import ProfileSecretDto
from lava_sdk.exceptions.profile.profile_exception import ProfileException
from lava_sdk.http.lava_facade import LavaFacade
from tests.Mocks.client_error_response_mock import ClientErrorResponseMock
from tests.Mocks.client_success_response_mock import ClientSuccessResponseMock


def _make_facade(client):
    profile_data = ProfileSecretDto(str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()))
    return LavaFacade(
        str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()),
        client=client, profile_secret_data=profile_data
    )


def test_get_profile_balance_success():
    facade = _make_facade(ClientSuccessResponseMock())
    response = facade.get_profile_balance()
    assert isinstance(response, ProfileBalanceDto)
    assert response.get_total_balance() == 10000
    assert response.get_available_balance() == 8000
    assert response.get_freeze_balance() == 2000


def test_get_profile_balance_error():
    facade = _make_facade(ClientErrorResponseMock())
    with pytest.raises(ProfileException):
        facade.get_profile_balance()
