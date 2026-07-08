from abc import ABC

from fastapi import Request

from pyrannic.contracts.application import ApplicationInterface


class RequestInterface(ABC, Request):
    """
    This interface extends the FastAPI Request class and can be used to define custom request properties or methods that are specific to the application's needs.
    By using this interface, you can ensure that all request objects in your application adhere to a consistent structure and provide the necessary functionality for your application's requirements.
    """

    @property
    def app(self) -> ApplicationInterface:
        return super().app
