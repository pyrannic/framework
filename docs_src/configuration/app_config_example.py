from pydantic import Field

from pyrannic import Configuration


class AppConfig(Configuration):
    name: str = Field(default="Pyrannic")
    """This value is the name of your application, which will be used when the framework needs to place the
    application's name in a notification or other UI elements where an application name needs to be displayed."""

    env: str = Field(default="production")
    """This value determines the 'environment' your application is currently running in.
    This may determine how you prefer to configure various services the application utilizes. Set this in your '.env' file."""

    debug: bool = Field(default=False)
    """When your application is in debug mode, detailed error messages with
    stack traces will be shown on every error that occurs within your
    application. If disabled, a simple generic error page is shown."""
