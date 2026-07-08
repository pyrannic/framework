from pyrannic.contracts.config.respository import ConfigRepositoryInterface


def test_all_method(repository: ConfigRepositoryInterface):
    config = repository.all()

    assert isinstance(config, dict)
    assert config is not None
    assert config["database"]["host"] == "localhost"
    assert config["database"]["port"] == 5432
    assert config["database"]["username"] == "user"
    assert config["database"]["password"] == "pass"
    assert config["app"]["name"] == "MyApp"
    assert config["app"]["debug"] is True
    assert config["app"]["secret_key"] == "supersecret"
