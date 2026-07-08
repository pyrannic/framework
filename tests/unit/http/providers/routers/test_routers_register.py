from pyrannic.contracts.application import ApplicationInterface
from pyrannic.http.providers import RoutersServiceProvider


def test_register_using_provider(application: ApplicationInterface):
    provider = RoutersServiceProvider(application)
    provider.register()

    assert application.router.url_path_for("get_object_memory_address")
    assert application.router.url_path_for("get_scoped_memory_address")
    assert application.router.url_path_for("get_singleton_memory_address")


def test_register_without_providers(app_no_providers: ApplicationInterface):
    provider = RoutersServiceProvider(app_no_providers)
    provider.register()

    assert app_no_providers.router.url_path_for("get_object_memory_address")
    assert app_no_providers.router.url_path_for("get_scoped_memory_address")
    assert app_no_providers.router.url_path_for("get_singleton_memory_address")
