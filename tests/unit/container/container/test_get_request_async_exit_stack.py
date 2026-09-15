from contextlib import AsyncExitStack

from fastapi import Request

from pyrannic.container.container import Container


def _build_request() -> Request:
    return Request({"type": "http"})


def test_get_request_async_exit_stack_uses_state_stack_when_available(
    container: Container,
):
    request = _build_request()
    existing_stack = AsyncExitStack()
    request.state._pyrannic_async_exit_stack = existing_stack

    stack = container._get_request_async_exit_stack(request)  # pyright: ignore[reportPrivateUsage]

    assert isinstance(stack, AsyncExitStack)
    assert stack is existing_stack


def test_get_request_async_exit_stack_creates_and_stores_fallback_stack(
    container: Container,
):
    request = _build_request()

    stack = container._get_request_async_exit_stack(request)  # pyright: ignore[reportPrivateUsage]

    assert isinstance(stack, AsyncExitStack)
    assert request.state._pyrannic_async_exit_stack is stack


def test_get_request_async_exit_stack_reuses_created_fallback_stack(
    container: Container,
):
    request = _build_request()

    first_stack = container._get_request_async_exit_stack(request)  # pyright: ignore[reportPrivateUsage]
    second_stack = container._get_request_async_exit_stack(request)  # pyright: ignore[reportPrivateUsage]

    assert isinstance(first_stack, AsyncExitStack)
    assert second_stack is first_stack
