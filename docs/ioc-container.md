## Introduction

Managing class dependencies and executing dependency injection is made efficient through the powerful *Pyrannic* IoC container.
While it may sound complex, dependency injection simply refers to the process where a class receives its dependencies from an external source, typically through its constructor or specialized "setter" methods.

To illustrate this concept, consider the following basic example:

```python
--8<-- "docs_src/ioc_container/basic_01_example.py"
```

In this example, the `/heroes` route needs to retrieve a collection of heroes from a data source such as `HeroesServiceInterface`. So, we will inject a service that is able to retrieve heroes. Since the service is injected, we are able to easily "mock", or create a dummy implementation of the `HeroesServiceInterface` service when testing our application.

To construct robust, large-scale applications or contribute to the core of *Pyrannic*, it is vital to have a thorough grasp of its IoC container.

### When to Utilize the Container

In many cases, thanks to the default dependency injection provided by *FastAPI*, you can build *Pyrannic* applications without ever manually binding or resolving anything from the container. So, when would you ever manually interact with the *Pyrannic* IoC Container? Let's examine two situations.

First, if you write a class that implements an interface and you wish to use that interface on a route or class constructor, you must tell the container how to resolve that interface.

Furthermore, unlike *FastAPI's* standard dependency injection, which restricts cached instances to a single request, *Pyrannic* enables caching across the entire application lifecycle. This capability allows you to effectively implement *singleton* instances for your classes.

## Binding

### Binding Basics

Almost all of your IoC container bindings will be registered within service providers, so most of these examples will demonstrate using the container in that context.

Within a service provider, you always have access to the container via the `container` property. We can register a binding using the `bind` method, passing the class or interface `type` that we wish to register along with a `Callable` that returns an instance of the class:

```python
--8<-- "docs_src/ioc_container/bind_example.py"
```

Note that we receive the app itself as an argument to the resolver. We can then use the container from it to resolve sub-dependencies of the object we are building.

You may use the `bind_if` method to register a container binding only if a binding has not already been registered for the given type:

```python
--8<-- "docs_src/ioc_container/bind_if_example.py"
```

!!! warning "Bind things just when needed"
    There is no need to bind classes into the container if they do not depend on any interfaces.
    The container does not need to be instructed on how to build these objects, since it can automatically resolve these objects.
    Check [When to Utilize the Container](#when-to-utilize-the-container) to know more.

#### Binding a Singleton

The `singleton` method binds a class or interface into the container that should only be resolved one time. Once a singleton binding is resolved, the same object instance will be returned on subsequent calls into the container during all the lifecycle of the application:

```python
--8<-- "docs_src/ioc_container/singleton_example.py"
```

You may use the `singleton_if` method to register a singleton container binding only if a binding has not already been registered for the given type:

```python
--8<-- "docs_src/ioc_container/singleton_if_example.py"
```

##### Singleton Decorator

Alternatively, you may mark an interface or class with the `@singleton` decorator to indicate to the container that it should be resolved one time during all the lifecycle of the application:

```python
--8<-- "docs_src/ioc_container/singleton_decorator_example.py"
```

#### Binding Scoped Singletons

The `scoped` method binds a class or interface into the container that should only be resolved one time within a given Pyrannic request. While this method is similar to the `singleton` method, instances registered using the `scoped` method will be flushed whenever the Pyrannic application starts a new "lifecycle", such as when a FastAPI processes a new request:

```python
--8<-- "docs_src/ioc_container/scoped_example.py"
```

You may use the `scoped_if` method to register a scoped container binding only if a binding has not already been registered for the given type:

```python
--8<-- "docs_src/ioc_container/scoped_if_example.py"
```

##### Scoped Decorator

Alternatively, you may mark an interface or class with the `@scoped` decorator to indicate to the container that it should be resolved one time within a given Pyrannic/FastAPI request lifecycle:

```python
--8<-- "docs_src/ioc_container/scoped_decorator_example.py"
```

#### Binding Instances

You may also bind an existing object instance into the container using the `instance` method. The given instance will always be returned on subsequent calls into the container:

```python
--8<-- "docs_src/ioc_container/instance_example.py"
```

### Binding Interfaces to Implementations

A very powerful feature of the service container is its ability to bind an interface to a given implementation. For example, let's assume we have an `EventPusher` interface and a `RedisEventPusher` implementation. Once we have coded our `RedisEventPusher` implementation of this interface, we can register it with the service container like so:

```python
--8<-- "docs_src/ioc_container/interface_01_example.py"
```

This statement tells the container that it should inject the `RedisEventPusher` when a class needs an implementation of `EventPusher`. Now we can type-hint the `EventPusher` interface in the constructor of a class or any other `Callable` that is resolved by the container:

```python
--8<-- "docs_src/ioc_container/interface_02_example.py"
```

Because the `RedisEventPusher` is resolved by the container, you can use its constructor to inject any dependency that you could need. They will be resolved recursively once the container creates the class instance:

```python
--8<-- "docs_src/ioc_container/interface_03_example.py"
```

!!! tip "Know More"
    Note above how we are using `Depends` function provided by FastAPI. You can mix the *Pyrannic* IoC container with the dependecy injection system of *FastAPI*

### Contextual Binding

Pyrannic offers a straightforward and fluent way to handle scenarios where multiple classes use the same interface but require different implementation injections. Check the next example:

```python
--8<-- "docs_src/ioc_container/contextual_binding_example.py"
```

Here, you can see how we have three services using the `FilesystemInterface` and how we can declare which implementation to use on each of them.

## Resolving

### The `resolve` Method

You may use the `resolve` method to resolve a class instance from the container. The make method accepts the `type` of the class or interface you wish to resolve:

```python
--8<-- "docs_src/ioc_container/resolve_example.py"
```

If you used an `string` to bind your class or interface or you setup an alias, you can use also that string with the `resolve` method:

```python
--8<-- "docs_src/ioc_container/resolve_with_string_example.py"
```

!!! abstract "Refering to an abstract"
    All methods in the container that accept a `type` to refer to an abstract, can accept an `string` too.

The `bound` method may be used to determine if a class or interface has been explicitly bound in the container:

```python
--8<-- "docs_src/ioc_container/bound_example.py"
```

### Automatic Injection

Alternatively, and importantly, you can also use `Annotated` and `Resolves` to type-hint dependencies within the constructor of any class or any other type of `Callable` resolved by the container, such as routes and middlewares. This approach represents the standard method for object resolution within the container in practice.

For example, you may type-hint a service defined by your application in a route's function. The service will automatically be resolved and injected into the class:

```python hl_lines="13"
--8<-- "docs_src/ioc_container/basic_01_example.py"
```

As a shorthand version, you can use the `Resolve` annotation:

```python hl_lines="13"
--8<-- "docs_src/ioc_container/basic_02_example.py"
```

## Method Invocation and Injection

You might occasionally need to execute a method on an object instance and have the container handle the automatic injection of that method's dependencies. To illustrate this, consider the class below:

```python hl_lines="8"
--8<-- "docs_src/ioc_container/hero_stats.py"
```

You may invoke the `generate` method via the container like so:

```python hl_lines="2"
--8<-- "docs_src/ioc_container/call_example.py"
```

!!! info "The `call` method"
    The `call` method is an `async` method and accepts any Python callable, `Callable[..., Any]`

