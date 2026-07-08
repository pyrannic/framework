from typing import Annotated

from fastapi import Depends

from src.app.contracts import EventPusherInterface
from src.app.http.client import HttpClient


class RedisEventPusher(EventPusherInterface):
    def __init__(self, http_client: Annotated[HttpClient, Depends()]):
        pass
