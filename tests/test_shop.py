import uuid
import pytest

from lava_sdk.dto.response.shop.shop_balance_dto import ShopBalanceDto
from lava_sdk.exceptions.shop.shop_exception import ShopException
from lava_sdk.http.lava_facade import LavaFacade
from tests.Mocks.client_error_response_mock import ClientErrorResponseMock
from tests.Mocks.client_success_response_mock import ClientSuccessResponseMock


def test_get_shop_balance_success():
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=ClientSuccessResponseMock())
    response = facade.get_shop_balance()
    assert isinstance(response, ShopBalanceDto)
    assert response.get_balance() == 37500.08
    assert response.get_freeze_balance() == 375000.08


def test_get_shop_balance_fail():
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=ClientErrorResponseMock())
    with pytest.raises(ShopException) as exc_info:
        facade.get_shop_balance()
    assert exc_info.value.args[0] == "Field shopId is required"
