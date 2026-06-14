## Introduction

In general, when we talk about *bootstrapping*, we mean registering things, including registering IoC container bindings, event listeners, middleware and even routes.

In a *FastAPI* application, the bootstrapping is done using the [`lifespan` parameter](https://fastapi.tiangolo.com/advanced/events/#lifespan-function) of your *FastAPI* app:

```python title="Lifespan example from FastAPI documentation" hl_lines="22"
--8<-- "docs_src/bootstrap/lifespan_example.py"
```

In a little application, you can keep this logic in your `main.py` together to the initialization of your application. But as your app grows, the `lifespan` function also become increasingly large, so at some point, it will be needed to build a better implementation that decouples the lifespan logic from the `main.py`.

## The Bootstrapping Layer

To avoid having to create this bootstrapping layer in every application that you create, *Pyranninc* provides you this layer out-of-the-box. 

In this layer, *Providers* are the core to bootstrapping a *Pyrannic* application. When *Pyarannic* creates the *FastAPI* application instance, it passes as `lifespan` parameter an *async context manager* from the `BootstrapManager`. This manager is the responsible to register, initialize and boot (in that order) the registered providers.

Your application's user-defined providers are stored in the `app/providers` directory. By default, the AppServiceProvider is fairly empty. This provider is a great place to add your application's own bootstrapping and service container bindings.

Eventually, for large applications, you may wish to create several service providers, each with more granular bootstrapping for specific services used by your application. To know more about how to create your own service providers, you can check its [documentation here](service-providers.md).

## The Service Providers

A *Pyrannic* application knows which providers to use because they are registered in the module located in `bootstrap/provider.py`. There, there is a list which it is used to assign the providers that the application will need to use.

```python title="bootstrap/providers.py" hl_lines="13"
--8<-- "docs_src/bootstrap/providers.py"
```

In a fresh new application this list contains the common providers needed by an application, but you have totally freedom to customize the providers used by your application.

As an opinionated framework, *Pyrannic* gives you several conventions implemented for your convenience. But, in last instance, you decide if you want to use them or create custom solutions for your application.

For example, the routers and middlewares providers:

```python title="bootstrap/providers.py" hl_lines="7 8 17 18"
--8<-- "docs_src/bootstrap/providers.py"
```

Using the `RoutersServiceProvider` and the `MiddlewaresServiceProvider`, *Pyrannic* will decide for you that all the routers and all the middlewares must be located in one place (`app/http/routers` and `app/http/middlewares`, respectively). To know more about [routers](routers.md) and [middlewares](middlewares.md), please visit their documentation.
