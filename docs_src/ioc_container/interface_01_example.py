from src.app.contracts import EventPusherInterface
from src.app.services import RedisEventPusher

self.container.bind(EventPusherInterface, RedisEventPusher)
