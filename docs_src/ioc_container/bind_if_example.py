self.container.bind_if(
    SnowflakeService,
    lambda app, request: SnowflakeService(app.container.resolve(SnowflakeConfig)),
)
