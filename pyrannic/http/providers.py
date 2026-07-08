from inspect import isfunction
import os

from fastapi import APIRouter

from pyrannic.bootstrap.service_provider import ServiceProvider
from pyrannic.http.exceptions.resource_not_found import (
    ResourceNotFoundException,
    handle_resource_not_found_exception,
)
from pyrannic.http.exceptions.unprocessable_entity import (
    UnprocessableEntityException,
    handle_unprocessable_entity_exception,
)
from pyrannic.support.importing import import_modules
from pyrannic.support.path import get_module_paths
from pyrannic.support.reflection import get_attr, get_attrs, get_class, get_functions


class RoutersServiceProvider(ServiceProvider):
    def register(self):
        routers = get_attr(
            os.path.join(self.app.base_path, "bootstrap/routers"),
            "routers",
            [],
        )

        if not bool(routers):
            modules = get_module_paths(
                os.path.join(self.app.base_path, "app/http/routers")
            )
            routers: list[APIRouter] = get_attrs(modules, "router")

        for router in routers:
            self.app.include_router(router)


class MiddlewaresServiceProvider(ServiceProvider):
    def register(self):
        middlewares = get_attr(
            os.path.join(self.app.base_path, "bootstrap/middlewares"),
            "middlewares",
            [],
        )

        if middlewares:
            for middleware in middlewares:
                if isfunction(middleware):
                    self.app.middleware("http")(middleware)
                else:
                    self.app.add_middleware(middleware)
        else:
            for _, module in import_modules(
                os.path.join(self.app.base_path, "app/http/middlewares")
            ):
                middleware = get_class(
                    module,
                    class_suffix="Middleware",
                )

                if middleware:
                    self.app.add_middleware(middleware)
                else:
                    for _, middleware in get_functions(
                        module,
                        lambda name: not name.startswith("_"),
                    ):
                        self.app.middleware("http")(middleware)


class ExceptionHandlersServiceProvider(ServiceProvider):
    def register(self):
        self.app.add_exception_handler(
            UnprocessableEntityException, handle_unprocessable_entity_exception
        )
        self.app.add_exception_handler(
            ResourceNotFoundException, handle_resource_not_found_exception
        )
