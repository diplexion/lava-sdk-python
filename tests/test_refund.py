import uuid
import pytest

from lava_sdk.dto.request.refund.create_refund_dto import CreateRefundDto
from lava_sdk.dto.request.refund.get_status_refund_dto import GetStatusRefundDto
from lava_sdk.dto.response.refund.created_refund_dto import CreatedRefundDto
from lava_sdk.dto.response.refund.status_refund_dto import StatusRefundDto
from lava_sdk.exceptions.refund.refund_exception import RefundException
from lava_sdk.http.lava_facade import LavaFacade
from tests.Mocks.client_error_response_mock import ClientErrorResponseMock
from tests.Mocks.client_success_response_mock import ClientSuccessResponseMock


def test_create_refund_success():
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=ClientSuccessResponseMock())
    response = facade.create_refund(CreateRefundDto(str(uuid.uuid4())))
    assert isinstance(response, CreatedRefundDto)


def test_create_refund_fail():
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=ClientErrorResponseMock())
    with pytest.raises(RefundException) as exc_info:
        facade.create_refund(CreateRefundDto(str(uuid.uuid4())))
    assert exc_info.value.args[0] == "Invoice not found"


def test_get_status_refund_success():
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=ClientSuccessResponseMock())
    response = facade.check_status_refund(GetStatusRefundDto(str(uuid.uuid4())))
    assert isinstance(response, StatusRefundDto)


def test_get_status_refund_fail():
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=ClientErrorResponseMock())
    with pytest.raises(RefundException) as exc_info:
        facade.check_status_refund(GetStatusRefundDto(str(uuid.uuid4())))
    assert exc_info.value.args[0] == "Refund not found"
