from pyrannic.contracts.config.repository import ConfigRepositoryInterface


def test_optional_bool(repository: ConfigRepositoryInterface):
    assert repository.optional_bool("foo.boolean") is True
    assert repository.optional_bool("foo.non_existent_key") is None
    assert repository.optional_bool("foo.non_existent_key", False) is False


def test_bool(repository: ConfigRepositoryInterface):
    assert repository.bool("foo.boolean") is True
    assert repository.bool("foo.non_existent_key") is False
    assert repository.bool("foo.non_existent_key", True) is True


def test_bool_truthy_strings(repository: ConfigRepositoryInterface):
    assert repository.bool("foo.boolean_true") is True
    assert repository.bool("foo.boolean_True") is True
    assert repository.bool("foo.boolean_TRUE") is True

    assert repository.bool("foo.boolean_yes") is True
    assert repository.bool("foo.boolean_Yes") is True
    assert repository.bool("foo.boolean_YES") is True

    assert repository.bool("foo.boolean_one") is True


def test_bool_falsy_strings(repository: ConfigRepositoryInterface):
    assert repository.bool("foo.boolean_false") is False
    assert repository.bool("foo.boolean_False") is False
    assert repository.bool("foo.boolean_FALSE") is False

    assert repository.bool("foo.boolean_no") is False
    assert repository.bool("foo.boolean_No") is False
    assert repository.bool("foo.boolean_NO") is False

    assert repository.bool("foo.boolean_zero") is False


def test_bool_integer(repository: ConfigRepositoryInterface):
    assert repository.bool("foo.boolean_int_0") is False
    assert repository.bool("foo.boolean_int_1") is True
