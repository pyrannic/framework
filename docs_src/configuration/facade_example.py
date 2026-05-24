from pyrannic import Config


def my_function():
    value = Config.get("app.debug")
    ...
    ...
