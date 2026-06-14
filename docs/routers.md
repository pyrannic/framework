## Default Service Provider

Pyrannic provides you a service provider which can be used to register automatically your routers.

```python title="bootstrap/providers.py" hl_lines="8 17"
--8<-- "docs_src/bootstrap/providers.py"
```

With this provider, Pyrannic will get all your modules from the path `app/http/routers` and search for a `router` attribute:

```python title="app/http/routers/heroes.py" hl_lines="8"
--8<-- "docs_src/routers/router_example.py"
```

### Bootstrapping File

By default, the provider will register your routers by alphabetic order of the module's name.

But, if you need it, you can customise the order of the registration of your routers creating a new file `routers.py` in the `bootstrap` folder of your app. The provider will read the `routers` list from this file and use it to register them.

```python title="bootstrap/routers.py" hl_lines="7"
--8<-- "docs_src/routers/routers_example.py"
```

## Custom Service Provider

To use the default service provider from Pyrannic **is not mandatory**. You can write your own service provider and register your routes just like you would do it normally in FastAPI.

```python title="Custom RoutersServiceProvider" hl_lines="8 9"
--8<-- "docs_src/service_providers/routers_service_providers.py"
```

!!! abstract "The property app"
    The `ServiceProvider` give you access to the underneath application throw the property `app`.
    This property is an instance of an `ApplicationInterface` but, in the end, it is also an instance of a FastAPI application,
    and you can use all its methods. To know more about the service providers check [its documentation](service-providers.md).
