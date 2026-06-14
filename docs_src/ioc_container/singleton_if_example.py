self.container.singleton_if(
    SnowflakeService,
    lambda app, request: SnowflakeService(app.container.resolve(SnowflakeConfig)),
)
