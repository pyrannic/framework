from pyrannic.contracts.config.repository import ConfigRepositoryInterface


def test_optional_str(repository: ConfigRepositoryInterface):
    assert repository.optional_str("database.port") == "5432"
    assert repository.optional_str("database.non_existent_key") is None
    assert repository.optional_str("database.non_existent_key", "default") == "default"
    assert repository.optional_str("foo.integer_str") == "42"


def test_str(repository: ConfigRepositoryInterface):
    assert repository.str("database.port") == "5432"
    assert repository.str("database.non_existent_key") == ""
    assert repository.str("database.non_existent_key", "default") == "default"
    assert repository.str("foo.integer_str") == "42"


def test_str_with_non_string_value(repository: ConfigRepositoryInterface):
    assert repository.str("app.debug") == "True"
    assert repository.optional_str("app.debug") == "True"
