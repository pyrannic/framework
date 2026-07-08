from src.app.snowflake import SnowflakeService, SnowflakeConfig

self.container.scoped(
    SnowflakeService,
    lambda app, request: SnowflakeService(app.container.resolve(SnowflakeConfig)),
)
