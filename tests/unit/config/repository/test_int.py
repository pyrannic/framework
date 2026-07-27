from pyrannic.contracts.config.repository import ConfigRepositoryInterface


def test_optional_int(repository: ConfigRepositoryInterface):
    assert repository.optional_int("database.port") == 5432
    assert repository.optional_int("database.non_existent_key") is None
    assert repository.optional_int("database.non_existent_key", 42) == 42
    assert repository.optional_int("foo.integer_str") == 42


def test_int(repository: ConfigRepositoryInterface):
    assert repository.int("database.port") == 5432
    assert repository.int("database.non_existent_key") == 0
    assert repository.int("database.non_existent_key", 42) == 42
    assert repository.int("foo.integer_str") == 42


def test_int_with_non_integer_value(repository: ConfigRepositoryInterface):
    assert repository.int("app.name") == 0
    assert repository.optional_int("app.name") is None
