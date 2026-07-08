## Default Service Provider

Pyrannic makes available to you a service provider which can be used to register automatically your middlewares.

```python title="bootstrap/providers.py" hl_lines="7 18"
--8<-- "docs_src/bootstrap/providers.py"
```

This provider will get all your modules from the path `app/http/middlewares` and search for any public `function` or any public `class` and register them in the application.

### Bootstrapping File

By default, the provider will register your routers by alphabetic order of the module's name.
But, with middlewares, sometimes you will need more granularity in their registration, requiring an specific order between them.

You can customise this order in the registration of your middlewares creating a new file `middlewares.py` in the `bootstrap` folder of your app.
The provider will read the `middlewares` list from this file and use it to register them.

```python title="bootstrap/middlewares.py" hl_lines="7"
--8<-- "docs_src/middlewares/middlewares_example.py"
```

## Custom Service Provider

To use the default service provider from Pyrannic **is not mandatory**. You can write your own service provider and register your middlewares just like you would do it normally in FastAPI.

```python title="Custom MiddlewaresServiceProvider" hl_lines="8 9"
--8<-- "docs_src/middlewares/middlewares_service_providers.py"
```

!!! abstract "The property app"
    The `ServiceProvider` give you access to the underneath application through the `app` property.
    This property is an instance of an `ApplicationInterface` but, in the end, it is also an instance of a FastAPI application,
    and you can use all its methods. To know more about the service providers check [its documentation](service-providers.md).
