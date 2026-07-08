import os

from pyrannic.bootstrap.instance_service_provider import InstanceServiceProvider
from pyrannic.config.repository import ConfigRepository
from pyrannic.contracts.config.configuration import ConfigurationInterface
from pyrannic.contracts.config.respository import ConfigRepositoryInterface
from pyrannic.support.path import get_module_paths
from pyrannic.support.reflection import get_classes


class ConfigRepositoryProvider(InstanceServiceProvider[ConfigRepositoryInterface]):
    @property
    def aliases(self) -> list[str | type] | None:
        return ["config"]

    def _create(self) -> ConfigRepositoryInterface:
        repo = ConfigRepository()

        modules = get_module_paths(os.path.join(self.app.base_path, "config"))
        classes = get_classes(modules, class_suffix="Config")

        for cls in classes:
            instance: ConfigurationInterface = cls()
            repo.set(instance.config_key, instance.to_dict())

        return repo
