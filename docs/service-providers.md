## Introduction

One of the most important kernel bootstrapping actions is loading the service providers for your application. Service providers are responsible for bootstrapping all of the framework's various components, such as the database, exception handlers, middlewares, and routing components.

*Pyrannic* will iterate through this list of providers and instantiate each of them. After instantiating the providers, the `register` method will be called on all of the providers. Then, once all of the providers have been registered, the `initialize` method (which can be `async` if needed) will be called on each provider. Finally, after initialize all providers, the `boot` method (optional `async` too) will be executed on each provider. This is so service providers may depend on every container binding being registered and initialized and available by the time their boot method is executed.

Essentially every major feature offered by *Pyrannic* is bootstrapped and configured by a service provider. Since they bootstrap and configure so many features offered by the framework, service providers are the most important aspect of the entire *Pyrannic* bootstrap process.

While the framework internally uses dozens of service providers, you also have the option to create your own. You can find a list of the user-defined or third-party service providers that your application is using in the `bootstrap/providers.py` file.

!!! abstract
    If you would like to learn more about how *Pyrannic* handles the bootstrapping and how it works internally, check out our documentation on the [*Pyrannic* boostrap](bootstrap.md).

## Writing Service Providers

All service providers extend the `ServiceProvider` class. Most service providers contain a `register`, an `initialize` and/or a `boot` method.

```python hl_lines="4"
--8<-- "docs_src/service_providers/routers_service_providers.py"
```

Within the `register` method, you can bind things into the [IoC container](ioc-container.md) as well as register routes, middlewares, exception handlers or any other piece of functionality that needs to be configured before the underneath *FastAPI* app is initialized.

### The `register` Method

As mentioned previously, within the `register` method, you should only bind things into the IoC container as well as any other piece of functionality related to the *FastAPI* app that needs to be configured before the application starts to run by the server.

**The method can't be `async` and you can't use it to inject dependencies**. Otherwise, you may accidentally use a service that is provided by a service provider which has not loaded yet.

Let's take a look at a basic service provider. Within any of your service provider methods, you always have access to the `app` property which provides access to the *FastAPI* application:

```python hl_lines="6 7"
--8<-- "docs_src/service_providers/routers_service_providers.py"
```

This service provider only defines a `register` method, and uses that method to include a router into the application.

```python hl_lines="8 9"
--8<-- "docs_src/service_providers/database_service_providers_001.py"
```

This other service provider defines also a `register` method, and uses that method to define an implementation of `DatabaseManagerInterface` in the service container. If you're not yet familiar with the *Pyrannic* IoC container, check out [its documentation](ioc-container.md).

#### The `__bindings__` and `__singletons__` Properties

If your service provider registers many simple bindings, you may wish to use the `__bindings__` and `__singletons__` properties instead of manually registering each container binding. When the service provider is loaded by the framework, it will automatically check for these properties and register their bindings:

```python hl_lines="10 11 12"
--8<-- "docs_src/service_providers/database_service_providers_002.py"
```

### The `initialize` Method

In certain scenarios, a provider may require the execution of asynchronous operations before it becomes fully operational and accessible to other components of the system.

This specialized asynchronous behavior cannot be accommodated within the `register` method, primarily because that method is executed outside of an active asynchronous context.

To address this, *Pyrannic* provides the `initialize` method. This method is specifically designed for `async` initialization tasks, ensuring that the application only proceeds once the provider is fully configured and ready for use. By leveraging this asynchronous workflow, developers can manage complex startup requirements without blocking the event loop or risking race conditions during the initial dependency injection phase.

The `initialize` method is perfect for performing critical operations such as:

- Running database migrations to ensure the schema is up to date before the service accepts requests.
- Executing database seeding for initial configuration or testing data.
- Establishing vital connections to cloud services, such as storage buckets.
- Performing IO operations like loading configuration files or pre-fetching remote assets.

This structured approach guarantees that all dependencies are in a healthy, initialized state before the application logic begins execution, providing a robust foundation for scalable systems.

### The `boot` Method

So, what if we need some dependency within our service provider? This should be done within the `boot` method. This method is called after all other service providers have been registered and initialized, meaning you have access to all other services that have been registered and initialized by the framework. You may inject dependencies for your provider's boot method. The [IoC container](ioc-container.md) will automatically inject any dependencies you need:

```python hl_lines="14 15"
--8<-- "docs_src/service_providers/database_service_providers_003.py"
```

!!! info
    Note that, as the `initialize` method, the `boot` method can also be `async`, so you can do asynchronous operations inside your `boot` method.

### The `shutdown` Method

When the application begins its shutdown sequence, *Pyrannic* systematically iterates through every registered provider. During this cycle, it invokes the `shutdown` method for each one.

The `shutdown` method serves as a critical hook where developers can implement logic to gracefully free up resources or close connections utilized by their providers, ensuring a clean termination of the application.

```python hl_lines="17 18"
--8<-- "docs_src/service_providers/database_service_providers_004.py"
```

!!! info
    Note that, as the `initialize` and `boot` methods, the `shutdown` method can also be `async`.

## Registering Providers

All providers are registered in the `bootstrap/providers.py` configuration file. This file contains a list called `providers` that holds the classes of your application's service providers:

```python title="bootstrap/providers.py" hl_lines="13"
--8<-- "docs_src/service_providers/providers.py"
```

If you create a service provider, you must add the provider class to the list so it gets loaded:

```python title="bootstrap/providers.py" hl_lines="4 20"
--8<-- "docs_src/service_providers/custom_provider.py"
```