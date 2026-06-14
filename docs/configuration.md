## Introduction

All of the configuration files for the Pyrannic framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you.

These configuration files allow you to configure things like your database connection information as well as various other core configuration values such as your application name, application environment and enable/disable the debug mode.

## Overriding Config Values

In Pyrannic, the default implementation for the configuration system is done using Pydantic models, especifically **Pydantic Settings models**.
You can use standard Pydantic fields and read their values from your `.env` file.

Next, you can see the `app.py` config file:

```python title="config/app.py" hl_lines="7 11 15"
--8<-- "docs_src/configuration/app_config_example.py"
```

To override these configuration fields, you should use a `.env` file, as follows:

```shell
--8<-- "docs_src/configuration/env_example"
```

!!! info "Overrinding Environment Variables"
    Any variable in your `.env` file can be overridden by external environment variables such as server-level or system-level environment variables.

As an opinionated framework, Pyrannic has some conventions to configure its internal operation.
In this case, the default implementation for the configuration system requires that the env keys follow the next rules:

- They must be **uppercase**
- They must be **prefixed** with the config *category*. By default, this prefix is the filename of the config file (like in *app.py*, who prefix is *APP_*), but this is overriden in other config files using the property `env_prefix`, like in *logging.py* or *database.py*.

```python title="config/logging.py" hl_lines="19 20 21"
--8<-- "docs_src/configuration/logging_config_example.py"
```

## Accessing Config Values

You may easily access your configuration values injecting the `ConfigRepositoryInterface` in your code or using the `Config` facade from anywhere in your application.

### Using the Repository

The main way to access config values is the *Config Repository* through the `ConfigRepositoryInterface`
using the [IoC Container](ioc-container.md) from Pyrannic.

```python title="Injecting the ConfigRepositoryInterface" hl_lines="6"
--8<-- "docs_src/configuration/repo_example.py"
```

Note how the dependency injection is done using the `Resolves` function from Pyrannic instead the `Depends` function from FastAPI.
This is because the Pyrannic IoC Container supports abstract classes, while the FastAPI container doesn't.

!!! abstract "Know More"
    You can check the documentation of the [IoC Container](ioc-container.md) to know more about it and the internal architecture of Pyrannic.

### Using the Facade

As an alternative to the repository injection, you can use a `Facade`, the `Config` Facade.

```python title="Importing and Using the Config Facade" hl_lines="5"
--8<-- "docs_src/configuration/facade_example.py"
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

!!! abstract
    Currently, *Pyrannic* features only the `Config` facade. However, the roadmap includes plans for several additional facades, which is why it is important to keep the earlier warning in mind.


### Retrieval Methods

The configuration values may be accessed using *dot* syntax, which includes the name of the file and option you wish to access.
A default value may also be specified and will be returned if the configuration option does not exist:

```python
--8<-- "docs_src/configuration/retrieval_methods_example.py"
```

To assist with static analysis, the `ConfigRepositoryInterface` and `Config` facade also provides typed configuration retrieval methods. If the retrieved configuration value does not match the expected type, the default value will be returned:

```python
--8<-- "docs_src/configuration/retrieval_methods_2_example.py"
```

Also, there are the *optional* counterparts of those methods, which allow you to use `None` values, both in the default parameter and in the return value:

```python
--8<-- "docs_src/configuration/retrieval_methods_3_example.py"
```

## Behind the Scenes

The previous Pydantic implementation is a convenience final implementation which will fit very well to the majority of projects.
But Pyrannic always tries to be agnostic in their architecture, and the configuration system is not an exception.

### ConfigurationInterface

If you want or need it, you can use other configuration approach. For that, you only need to implement your config files inheriting from the parent class `ConfigurationInterface`.
This interface requires the implementation of one property and one method. Below you can see an example of a custom configuration implementation of the `app.py` configuration file.

```python
--8<-- "docs_src/configuration/config_interface_example.py"
```

### ConfigRepositoryInterface

The customization can be applied not only to the configuration files. If you need it, you can write your own `ConfigRepository` implementing the `ConfigRepositoryInterface`.

```python
--8<-- "docs_src/configuration/config_repo_interface_example.py"
```

TODO

### Service Provider

Once you have your repository implemented, you can register it using a service provider

TODO
