from pyrannic.contracts.config.respository import ConfigRepositoryInterface


def test_optional_float(repository: ConfigRepositoryInterface):
    assert repository.optional_float("foo.float") == 3.14
    assert repository.optional_float("foo.non_existent_key") is None
    assert repository.optional_float("foo.non_existent_key", 1.23) == 1.23
    assert repository.optional_float("foo.float_str") == 2.718


def test_float(repository: ConfigRepositoryInterface):
    assert repository.float("foo.float") == 3.14
    assert repository.float("foo.non_existent_key") == 0.0
    assert repository.float("foo.non_existent_key", 1.23) == 1.23
    assert repository.float("foo.float_str") == 2.718


def test_float_with_non_float_value(repository: ConfigRepositoryInterface):
    assert repository.float("app.name") == 0.0
    assert repository.optional_float("app.name") is None
