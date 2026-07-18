value1 = Config.get("app.debug")
value2 = config_repository.get("app.debug")

# Retrieve a default value if the configuration value does not exist.
value3 = Config.get("app.debug", True)
value4 = config_repository.get("app.debug", True)
