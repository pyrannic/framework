from pyrannic.contracts.application import ApplicationInterface
from pyrannic.http.exceptions.resource_not_found import ResourceNotFoundException
from pyrannic.http.exceptions.unprocessable_entity import UnprocessableEntityException
from pyrannic.http.providers import ExceptionHandlersServiceProvider


def test_exception_handlers_register(application: ApplicationInterface):
    provider = ExceptionHandlersServiceProvider(application)
    provider.register()

    assert application.exception_handlers is not None
    assert application.exception_handlers[UnprocessableEntityException] is not None
    assert application.exception_handlers[ResourceNotFoundException] is not None
