from pyrannic.contracts.application import ApplicationInterface
from pyrannic.http.providers import MiddlewaresServiceProvider


def test_register(application: ApplicationInterface):
    count = len(application.user_middleware)

    provider = MiddlewaresServiceProvider(application)
    provider.register()

    assert len(application.user_middleware) == count + 3


def test_register_without_providers(app_no_providers: ApplicationInterface):
    count = len(app_no_providers.user_middleware)

    provider = MiddlewaresServiceProvider(app_no_providers)
    provider.register()

    assert len(app_no_providers.user_middleware) == count + 3
