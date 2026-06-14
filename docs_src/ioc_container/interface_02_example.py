from typing import Annotated

from fastapi import APIRouter

from pyrannic import Resolves

from src.app.http.resources.event import EventsCollection
from src.app.contracts import EventPusherInterface

router = APIRouter()


@router.get("/events/queued")
def queued(service: Annotated[EventPusherInterface, Resolves()]) -> EventsCollection:
    return EventsCollection(service.queued_events())
