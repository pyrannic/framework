from pyrannic.contracts.config.respository import ConfigRepositoryInterface


def test_set_a_new_key(repository: ConfigRepositoryInterface):
    assert repository.get("app.my_key") is None
    repository.set("app.my_key", "my_value")
    assert repository.get("app.my_key") == "my_value"


def test_set_an_existing_key(repository: ConfigRepositoryInterface):
    assert repository.get("app.name") == "MyApp"
    repository.set("app.name", "MyNewApp")
    assert repository.get("app.name") == "MyNewApp"


def test_setattr_a_new_key(repository: ConfigRepositoryInterface):
    assert repository.get("app.my_key") is None
    setattr(repository, "app.my_key", "my_value")
    assert repository.get("app.my_key") == "my_value"


def test_setattr_an_existing_key(repository: ConfigRepositoryInterface):
    assert repository.get("app.name") == "MyApp"
    setattr(repository, "app.name", "MyNewApp")
    assert repository.get("app.name") == "MyNewApp"
