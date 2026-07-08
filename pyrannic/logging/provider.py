import logging
from logging import Logger

from pyrannic.bootstrap.instance_service_provider import InstanceServiceProvider
from pyrannic.support.facades.config import Config


class LoggingServiceProvider(InstanceServiceProvider[Logger]):
    @property
    def aliases(self) -> list[str | type] | None:
        return ["log"]

    def _create(self) -> Logger:
        logger = Logger("log")
        logger.setLevel(Config.integer("logging.level", logging.DEBUG))

        handlers = Config.list("logging.handlers", [logging.StreamHandler()])
        for handler in handlers:
            logger.addHandler(handler)

        return logger
