from pyrannic import Config


def my_function():
    unused_value = Config.get("app.debug")
    ...
    ...
