import uuid
import pytest

from lava_sdk.dto.request.invoice.create_invoice_dto import CreateInvoiceDto
from lava_sdk.dto.request.invoice.get_status_invoice_dto import GetStatusInvoiceDto
from lava_sdk.dto.response.invoice.created_invoice_dto import CreatedInvoiceDto
from lava_sdk.dto.response.invoice.status_invoice_dto import StatusInvoiceDto
from lava_sdk.exceptions.invoice.invoice_exception import InvoiceException
from lava_sdk.http.lava_facade import LavaFacade
from tests.Mocks.client_error_response_mock import ClientErrorResponseMock
from tests.Mocks.client_success_response_mock import ClientSuccessResponseMock


def test_create_invoice_success():
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=ClientSuccessResponseMock())
    response = facade.create_invoice(CreateInvoiceDto("300", str(uuid.uuid4())))
    assert isinstance(response, CreatedInvoiceDto)


def test_create_invoice_fail():
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=ClientErrorResponseMock())
    with pytest.raises(InvoiceException) as exc_info:
        facade.create_invoice(CreateInvoiceDto("300", str(uuid.uuid4())))
    assert exc_info.value.args[0] == "OrderId must be uniq"


def test_get_status_invoice_success():
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=ClientSuccessResponseMock())
    response = facade.check_status_invoice(GetStatusInvoiceDto(invoice_id=str(uuid.uuid4())))
    assert isinstance(response, StatusInvoiceDto)


def test_get_status_invoice_fail():
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=ClientErrorResponseMock())
    with pytest.raises(Exception) as exc_info:
        facade.check_status_invoice(GetStatusInvoiceDto(invoice_id=str(uuid.uuid4())))
    assert exc_info.value.args[0] == "Invoice not found"
