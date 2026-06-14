from src.app.snowflake import SnowflakeService, SnowflakeConfig

self.container.bind(
    SnowflakeService,
    lambda app, request: SnowflakeService(app.container.resolve(SnowflakeConfig)),
)
