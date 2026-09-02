from pyrannic.config.configuration import Configuration


class DatabaseConfig(Configuration):
    @property
    def env_prefix(self) -> str:
        return "DB_"
