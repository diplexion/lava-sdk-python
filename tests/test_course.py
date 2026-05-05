import uuid
import pytest

from lava_sdk.dto.response.course.course_dto import CourseDto
from lava_sdk.dto.response.course.currency_dto import CurrencyDto
from lava_sdk.exceptions.course.course_exception import CourseException
from lava_sdk.http.lava_facade import LavaFacade
from tests.Mocks.client_error_response_mock import ClientErrorResponseMock
from tests.Mocks.client_success_response_mock import ClientSuccessResponseMock


def _validate(course_list):
    assert isinstance(course_list, list)
    for item in course_list:
        assert isinstance(item, CourseDto)
        assert isinstance(item.get_currency(), CurrencyDto)
        assert isinstance(item.get_currency().get_label(), str)
        assert isinstance(item.get_currency().get_symbol(), str)
        assert isinstance(item.get_currency().get_value(), str)
        assert isinstance(item.get_value(), float)


def test_get_payoff_course_list_success():
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=ClientSuccessResponseMock())
    _validate(facade.get_payoff_course_list())


def test_get_payment_course_list_success():
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=ClientSuccessResponseMock())
    _validate(facade.get_payment_course_list())


def test_get_payment_course_list_fail():
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=ClientErrorResponseMock())
    with pytest.raises(CourseException):
        facade.get_payment_course_list()


def test_get_payoff_course_list_fail():
    facade = LavaFacade(str(uuid.uuid4()), str(uuid.uuid4()), client=ClientErrorResponseMock())
    with pytest.raises(CourseException):
        facade.get_payoff_course_list()
