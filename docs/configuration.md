## Introduction

All of the configuration files for the Pyrannic framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you.

These configuration files allow you to configure things like your database connection information as well as various other core configuration values such as your application name, application environment and enable/disable the debug mode.

## Overriding Config Values

In Pyrannic, the default implementation for the configuration system is done using Pydantic models, especifically **Pydantic Settings models**.
You can use standard Pydantic fields and read their values from your `.env` file.

Next, you can see the `app.py` config file:

```python title="config/app.py" hl_lines="7 11 15"
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
```

To override these configuration fields, you should use a `.env` file, as follows:

```shell
APP_NAME="MyAwesomeApp"
APP_ENV="development"
APP_DEBUG=True
```

!!! info "Overrinding Environment Variables"
    Any variable in your `.env` file can be overridden by external environment variables such as server-level or system-level environment variables.

As an opinionated framework, Pyrannic has some conventions to configure its internal operation.
In this case, the default implementation for the configuration system requires that the env keys follow the next rules:

- They must be **uppercase**
- They must be **prefixed** with the config *category*. By default, this prefix is the filename of the config file (like in *app.py*, who prefix is *APP_*), but this is overriden in other config files using the property `env_prefix`, like in *logging.py* or *database.py*.

```python title="config/logging.py" hl_lines="19 20 21"
import logging

from pydantic import Field

from pyrannic import Configuration


class LoggingConfig(Configuration):
    level: int = Field(default=logging.DEBUG)
    """The logging level to use for the application.
    This can be set to any of the standard logging levels (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)."""

    handlers: list[logging.Handler] = Field(
        default_factory=lambda: [logging.StreamHandler()]
    )
    """A list of logging handlers to use for the application.
    Handlers determine where the log messages are output, such as to the console, a file, or a remote logging server."""

    @property
    def env_prefix(self) -> str:
        return "LOG_"
```


## Accessing Config Values

You may easily access your configuration values injecting the `ConfigRepositoryInterface` in your code or using the `Config` facade from anywhere in your application.

### Using the Repository

The main way to access config values is the *Config Repository* through the `ConfigRepositoryInterface`
using the IoC Container from Pyrannic.

```python title="Injecting the ConfigRepositoryInterface" hl_lines="5"
from typing import Annotated
from pyrannic import Resolves
from pyrannic.contracts import ConfigRepositoryInterface

def resolver(config_repository: Annotated[ConfigRepositoryInterface, Resolves()]):
    value = config_repository.get("app.debug")
    ...
    ...
```

Note how the dependency injection is done using the `Resolves` function from Pyrannic instead the `Depends` function from FastAPI.
This is because the Pyrannic IoC Container supports abstract classes, while the FastAPI container doesn't.

!!! abstract "Know More"
    You can check the documentation of the [IoC Container](ioc-container.md) to know more about it and the internal archtecture of Pyrannic.

### Using the Facade

As an alternative to the repository injection, you can use a `Facade`, the `Config` Facade.

```python title="Importing and Using the Config Facade" hl_lines="4"
from pyrannic import Config

def my_function():
    value = Config.get("app.debug")
    ...
    ...
```

It has the exact same methods as the repository and it has the benefit that it can be used from anywhere in your application,
all this with less a verbose syntax because you don't need to inject it.

Because behind the scenes the facade uses the repository resolving the dependency through the *IoC Container*,
it is testable overrinding the repository dependency with mocks.

#### When to Utilize the Facade

Facades, in general, have many benefits. They provide a terse and memorable syntax that allows you to use some features
without remembering long class names that must be injected or configured manually.

However, some care must be taken when using facades. Since facades are so easy to use and do not require injection,
it can be easy to let your classes continue to grow and use many facades in a single class.
Using dependency injection, this potential is mitigated by the visual feedback a large constructor/function/method gives you
that your class is growing too large. So, when using facades, pay special attention to the size of your class so that its scope of responsibility stays narrow.
If your class is getting too large, consider splitting it into multiple smaller classes.

!!! tip
    Right now, Pyrannic only has a single one facade, the `Config` facade, but in the roadmap there are planned the addition of more.
    This is the reason to have in mind the previous *disclaimer*.

### Retrieval Methods

The configuration values may be accessed using *dot* syntax, which includes the name of the file and option you wish to access.
A default value may also be specified and will be returned if the configuration option does not exist:

```python
value = Config.get("app.debug")
value = config_repository.get("app.debug")

# Retrieve a default value if the configuration value does not exist.
value = Config.get("app.debug", True)
value = config_repository.get("app.debug", True)
```

To assist with static analysis, the `ConfigRepositoryInterface` and `Config` facade also provides typed configuration retrieval methods. If the retrieved configuration value does not match the expected type, the default value will be returned:

```python
Config.string('config-key')
Config.integer('config-key')
Config.float('config-key')
Config.boolean('config-key')
Config.array('config-key')
```

Also, there are the *optional* counterparts of those methods, which allow you to use `None` values, both in the default parameter and in the return value:

```python
Config.optional_string('config-key')
Config.optional_integer('config-key')
Config.optional_float('config-key')
Config.optional_boolean('config-key')
Config.optional_array('config-key')
```

## Behind the Scenes

The previous Pydantic implementation is a convenience final implementation which will fit very well to the majority of projects.
But Pyrannic always tries to be agnostic in their architecture, and the configuration system is not an exception.

### ConfigurationInterface

If you want or need it, you can use other configuration approach. For that, you only need to implement your config files inheriting from the parent class `ConfigurationInterface`.
This interface requires the implementation of one property and one method. Below you can see an example of a custom configuration implementation of the `app.py` configuration file.

```python
import os
from pyranninc.contracts import ConfigurationInterface

class AppConfig(ConfigurationInterface):
    @property
    def config_key(self) -> str:
        return "app"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": os.environ.get("app_name"),
            "env": os.environ.get("app_env"),
            "debug": True,
        }
```

### ConfigRepositoryInterface

The customization can be applied not only to the configuration files. If you need it, you can write your own `ConfigRepository` implementing the `ConfigRepositoryInterface`.

```python
import os
from pyranninc.contracts import ConfigRepositoryInterface

class ConfigRepository(ConfigRepositoryInterface):
    ...
    ...
```

TODO

### Service Provider

Once you have your repository implemented, you can register it using a service provider

TODO
