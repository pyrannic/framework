value = Config.get("app.debug")
value = config_repository.get("app.debug")

# Retrieve a default value if the configuration value does not exist.
value = Config.get("app.debug", True)
value = config_repository.get("app.debug", True)
