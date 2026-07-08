self.container.scoped_if(
    SnowflakeService,
    lambda app, request: SnowflakeService(app.container.resolve(SnowflakeConfig)),
)
