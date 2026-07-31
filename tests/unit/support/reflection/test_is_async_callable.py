import functools

from pyrannic.support.reflection import is_async_callable


class __MyClass:
    def __call__(self):
        pass


class __MyAsyncClass:
    async def __call__(self):
        pass


def __my_function():
    pass


async def __my_async_function():
    pass


def test_is_async_callable__check_async_function():
    """Test the is_async_callable function with an async function."""
    assert is_async_callable(__my_async_function) is True


def test_is_async_callable__check_sync_function():
    """Test the is_async_callable function with a sync function."""
    assert is_async_callable(__my_function) is False


def test_is_async_callable__check_async_class_instance():
    """Test the is_async_callable function with an async class instance."""
    assert is_async_callable(__MyAsyncClass()) is True


def test_is_async_callable__check_sync_class_instance():
    """Test the is_async_callable function with a sync class instance."""
    assert is_async_callable(__MyClass()) is False


def test_is_async_callable__check_async_class():
    """Test the is_async_callable function with an async class."""
    assert (
        is_async_callable(__MyAsyncClass) is False
    )  # Classes themselves are not async callable, only their instances can be.


def test_is_async_callable__check_sync_class():
    """Test the is_async_callable function with a sync class."""
    assert is_async_callable(__MyClass) is False


def test_is_async_callable__check_async_partial():
    """Test the is_async_callable function with a partial function."""
    partial_func = functools.partial(__my_async_function)
    assert is_async_callable(partial_func) is True


def test_is_async_callable__check_sync_partial():
    """Test the is_async_callable function with a sync partial function."""
    partial_func = functools.partial(__my_function)
    assert is_async_callable(partial_func) is False
