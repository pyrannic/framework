## Introduction

Complementing its built-in [authentication](/security/authentication) services, Pyrannic offers a structured and simple way to manage authorization checks, enabling you to easily validate user actions against specific resources. For instance, an authenticated user might still lack the permissions required to modify or remove specific database records or models within your application. To handle these validation requirements smoothly, Pyrannic delivers an organized and simple approach to managing authorization checks.

Pyrannic offers two main mechanisms for authorizing actions: [gates](#gates) and [policies](#policies). Gates deliver a straightforward, closure-based method for authorization. In contrast, policies organize authorization logic around a specific model or resource. This documentation will first explain gates before moving on to examine policies.

!!! abstract "Gates vs. Policies"
    Applications can use a combination of both gates and policies. Gates are best suited for actions that are not related to any specific model or resource (such as viewing an admin panel), while policies should be used to authorize actions for a particular model or resource.


## Gates

### Defining Gates

Gates are closures designed to verify whether a user has permission to execute a specific action. They are typically configured inside the **boot method** of the `ServiceProvider` class of your choice (e.g. your `AppServiceProvider`) injecting the `GateInterface`. Every gate receives a user instance as its primary argument and can accept further parameters, such as a corresponding ORM model.

For instance, to check if a user is allowed to update a given `Post` model, a gate can be defined to evaluate whether the user's `id` matches the `user_id` associated with the post's author:

```python hl_lines="8"
--8<-- "docs_src/security/authorization/defining_gates_example.py"
```

In the above example, we used a *lambda* to define the gate ability, but you could use any other type of `Callable`, like a *function* or a *class method*.

### Authorizing Actions

When authorizing actions with gates, use the `allows` or `denies` methods on the Gate. You do not need to manually pass the currently authenticated user, as *Pyrannic* automatically supplies the user to the gate closure. Typically, these authorization methods are called within your application's routers or services prior to executing an action that requires authorization.

```python hl_lines="8"
--8<-- "docs_src/security/authorization/authorizing_actions_example_01.py"
```

!!! danger "Work in Progress"
    This section is currently under development.

### Gate Responses

TODO

### Intercepting Gate Checks

TODO

### Inline Authorization

TODO

## Policies

### Creating Policies

### Registering Policies

### Defining Policies

#### Policy Methods
#### Policy Responses
#### Methods Without Models
#### Guest Users
#### Policy Filters

### Authorizing Actions
#### Via the User Model
#### Via the Gate Facade
#### Supplying Additional Context


!!! danger "Work in Progress"
    This section is currently under development and will be accessible very soon.
