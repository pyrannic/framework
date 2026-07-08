import importlib
from types import ModuleType
from typing import Any, Generator

from pyrannic.support.path import get_module_paths


def import_modules(package_path: str) -> Generator[tuple[str, ModuleType], Any, None]:
    """Imports a list of modules in a given package."""

    modules = get_module_paths(package_path)

    for module in modules:
        module_path = module.replace("\\", "/").replace("/", ".").replace(".py", "")
        module = importlib.import_module(module_path)

        yield module_path, module
