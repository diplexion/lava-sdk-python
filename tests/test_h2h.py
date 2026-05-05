import uuid
import pytest

from lava_sdk.dto.request.h2h.create_h2h_invoice_dto import CreateH2hInvoiceDto
from lava_sdk.dto.request.h2h.create_sbp_h2h_dto import CreateSBPH2HDto
from lava_sdk.dto.response.h2h.created_h2h_invoice_dto import CreatedH2hInvoiceDto
from lava_sdk.dto.response.h2h.created_sbp_h2h_dto import CreatedSBPH2hDto
from lava_sdk.exceptions.payoff.payoff_exception import PayoffException
from lava_sdk.http.lava_facade import LavaFacade
from tests.Mocks.client_error_response_mock import ClientErrorResponseMock
from tests.Mocks.client_success_response_mock import ClientSuccessResponseMock


def test_create_h2h_invoice_success():
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=ClientSuccessResponseMock())
    response = facade.create_h2h_invoice(
        CreateH2hInvoiceDto(100, str(uuid.uuid4()), 701, 11, 30, "5536914283728079")
    )
    assert isinstance(response, CreatedH2hInvoiceDto)


def test_create_h2h_invoice_fail():
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=ClientErrorResponseMock())
    with pytest.raises(PayoffException) as exc_info:
        facade.create_h2h_invoice(
            CreateH2hInvoiceDto(100, str(uuid.uuid4()), 701, 11, 30, "5536914283728079")
        )
    assert exc_info.value.args[0] == "Payment method was not found for this user"


def test_create_h2h_sbp_invoice_success():
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=ClientSuccessResponseMock())
    response = facade.create_h2h_spb_invoice(
        CreateSBPH2HDto(100, str(uuid.uuid4()), "127.0.0.1")
    )
    assert isinstance(response, CreatedSBPH2hDto)


def test_create_h2h_sbp_invoice_fail():
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=ClientErrorResponseMock())
    with pytest.raises(PayoffException) as exc_info:
        facade.create_h2h_spb_invoice(
            CreateSBPH2HDto(100, str(uuid.uuid4()), "127.0.0.1")
        )
    assert exc_info.value.args[0] == "Payment method was not found for this user"
