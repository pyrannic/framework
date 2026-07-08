from pyrannic.contracts.config.respository import ConfigRepositoryInterface


def test_optional_integer(repository: ConfigRepositoryInterface):
    assert repository.optional_integer("database.port") == 5432
    assert repository.optional_integer("database.non_existent_key") is None
    assert repository.optional_integer("database.non_existent_key", 42) == 42
    assert repository.optional_integer("foo.integer_str") == 42


def test_integer(repository: ConfigRepositoryInterface):
    assert repository.integer("database.port") == 5432
    assert repository.integer("database.non_existent_key") == 0
    assert repository.integer("database.non_existent_key", 42) == 42
    assert repository.integer("foo.integer_str") == 42


def test_integer_with_non_integer_value(repository: ConfigRepositoryInterface):
    assert repository.integer("app.name") == 0
    assert repository.optional_integer("app.name") is None
