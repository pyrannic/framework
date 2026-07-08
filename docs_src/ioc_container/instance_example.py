from src.app.snowflake import SnowflakeService, SnowflakeConfig

service = SnowflakeService(SnowflakeConfig())

self.container.instance(SnowflakeService, service)
