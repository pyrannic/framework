from pyrannic.contracts.config.respository import ConfigRepositoryInterface


def test_optional_boolean(repository: ConfigRepositoryInterface):
    assert repository.optional_boolean("foo.boolean") is True
    assert repository.optional_boolean("foo.non_existent_key") is None
    assert repository.optional_boolean("foo.non_existent_key", False) is False


def test_boolean(repository: ConfigRepositoryInterface):
    assert repository.boolean("foo.boolean") is True
    assert repository.boolean("foo.non_existent_key") is False
    assert repository.boolean("foo.non_existent_key", True) is True


def test_boolean_truthy_strings(repository: ConfigRepositoryInterface):
    assert repository.boolean("foo.boolean_true") is True
    assert repository.boolean("foo.boolean_True") is True
    assert repository.boolean("foo.boolean_TRUE") is True

    assert repository.boolean("foo.boolean_yes") is True
    assert repository.boolean("foo.boolean_Yes") is True
    assert repository.boolean("foo.boolean_YES") is True

    assert repository.boolean("foo.boolean_one") is True


def test_boolean_falsy_strings(repository: ConfigRepositoryInterface):
    assert repository.boolean("foo.boolean_false") is False
    assert repository.boolean("foo.boolean_False") is False
    assert repository.boolean("foo.boolean_FALSE") is False

    assert repository.boolean("foo.boolean_no") is False
    assert repository.boolean("foo.boolean_No") is False
    assert repository.boolean("foo.boolean_NO") is False

    assert repository.boolean("foo.boolean_zero") is False


def test_boolean_integer(repository: ConfigRepositoryInterface):
    assert repository.boolean("foo.boolean_int_0") is False
    assert repository.boolean("foo.boolean_int_1") is True
