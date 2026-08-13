## Introduction

Complementing its built-in [authentication](/security/authentication) services, Pyrannic offers a structured and simple way to manage authorization checks, enabling you to easily validate user actions against specific resources. For instance, an authenticated user might still lack the permissions required to modify or remove specific database records or models within your application. To handle these validation requirements smoothly, Pyrannic delivers an organized and simple approach to managing authorization checks.

Pyrannic offers two main mechanisms for authorizing actions: [abilities](#abilities) and [policies](#policies). Abilities deliver a straightforward, closure-based method for authorization. In contrast, policies organize authorization logic around a specific model or resource. This documentation will first explain abilities before moving on to examine policies.

!!! abstract "Abilities vs. Policies"
    Applications can use a combination of both abilities and policies. Abilities are best suited for actions that are not related to any specific model or resource (such as viewing an admin panel), while policies should be used to authorize actions for a particular model or resource.


## Abilities

### Defining Abilities

Abilities are closures designed to verify whether a user has permission to execute a specific action. They are typically configured inside the **boot method** of the `ServiceProvider` class of your choice (e.g. your `AppServiceProvider`) injecting the `GateInterface`. Every ability receives a user instance as its primary argument and can accept further parameters, such as a corresponding ORM model.

For instance, to check if a user is allowed to update a given `Post` model, an ability can be defined to evaluate whether the user's `id` matches the `user_id` associated with the post's author:

```python hl_lines="8"
--8<-- "docs_src/security/authorization/defining_abilities_example.py"
```

In the above example, we used a *lambda* to define the ability, but you could use any other type of `Callable`, like a *function* or a *class method*.

### Authorizing Actions {: #authorizing-actions--abilities}

When authorizing actions with abilities, use the `allows` or `denies` methods on the `Gate` interface. You do not need to manually pass the currently authenticated user, as *Pyrannic* automatically supplies the user to the ability closure. Typically, these authorization methods are called within your application's routers or services prior to executing an action that requires authorization:

```python title="app/http/routers/posts.py" hl_lines="31 32"
--8<-- "docs_src/security/authorization/authorizing_actions_example_01.py"
```

To check authorization for a user other than the one currently authenticated, call the `forUser` method provided by the `Gate` interface:

```python
--8<-- "docs_src/security/authorization/authorizing_actions_example_02.py"
```

To authorize multiple actions at a time, you can use the `any` or `none` methods:

```python
--8<-- "docs_src/security/authorization/authorizing_actions_example_03.py"
```

#### Authorizing or Throwing Exceptions

To authorize an action and automatically raise a `ForbiddenException` when a user lacks permission, use the `authorize` method provided by the `Gate` interface. *Pyrannic* automatically converts `ForbiddenException` instances into a 403 HTTP response.

```python
--8<-- "docs_src/security/authorization/authorize_example.py"
```

#### Providing Additional Context

The `Gate` methods for authorizing abilities (`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`) can receive extra arguments. These extra elements are passed as positional parameters or named parameters to the ability closure, and can be used for additional context when making authorization decisions:

```python hl_lines="1 6"
--8<-- "docs_src/security/authorization/additional_context_example.py"
```

### Gate Responses

!!! danger "Work in Progress"
    This section is currently under development.

### `before` and `after` callbacks

!!! danger "Work in Progress"
    This feature is currently under development.

### Inline Authorization

!!! danger "Work in Progress"
    This feature is currently under development.

## Policies

### Creating Policies

Policies organize authorization logic around specific models or resources. In a blog application, for instance, a `Post` model would pair with a `PostPolicy` to govern user permissions, such as creating or editing posts.

To create a policy, just put an empty class in `app/policies` or `app/models/policies`:

```python title="app/policies/post.py"
--8<-- "docs_src/security/authorization/creating_policies_example.py"
```

And that is all! Now we will see how to write a full policy.

### Registering Policies

#### Auto-discover

*Pyrannic* automatically discovers policies by default, provided that standard naming conventions are followed for both models and policies.
The models are placed in the `app/models` directory while the policies may be placed in the `app/policies` directory. In this situation, Pyrannic will check for policies in `app/models/policies` then `app/policies`. In addition, the policy name must match the model name and have a `Policy` suffix. So, a `User` model would correspond to a `UserPolicy` policy class.

In addition to this default behavior, you can define a custom logic for the policy discovery registering a callback via the `guess_policy_names_using` method from the `Gate` interface. You typically call this method within the `boot` method of your application's `AppServiceProvider` or other service provider of your choice:

```python title="app/providers/app.py"
--8<-- "docs_src/security/authorization/guess_policy_names_using_example.py"
```

#### Manually Registering

You can use the `define_policy` method from the `Gate` interface to manually register policies along with their corresponding models within the `boot` method of your application's `AppServiceProvider` (or other service provider):

```python title="app/providers/app.py"
--8<-- "docs_src/security/authorization/define_policy_example.py"
```

### Defining Policies

#### Policy Methods

After registering the policy class, you can define methods for each authorized action. For instance, an `update` method on the `PostPolicy` class can check whether a specific `User` is allowed to modify a given `Post` instance.

This `update` method will receive a `User` and a `Post` instance as parameters and returns a `boolean` value indicating authorization. In the following example, authorization is confirmed by verifying that the user's `id` matches the post's `user_id`:

```python title="app/policies/post.py"
--8<-- "docs_src/security/authorization/policy_methods_example.py"
```

You can define as many additional methods on the policy as needed to handle different authorized actions. While you might add standard methods like `view` or `delete` for managing Post actions, feel free to name your policy methods whatever works best for you.

!!! info "Dependencies in Policies"
    Because all policies are resolved through the Pyrannic service container, required dependencies can be type-hinted in the policy constructor for automatic injection.

#### Policy Responses

!!! danger "Work in Progress"
    This section is currently under development.

#### Methods Without Models

Certain policy methods require only an instance of the currently authenticated user. This scenario occurs most frequently when authorizing `create` actions. For instance, when building a blog, you might need to verify whether a user is permitted to create new posts. In such cases, your policy method should expect solely a user instance as its parameter:

```python title="app/policies/post.py"
--8<-- "docs_src/security/authorization/methods_without_models_example.py"
```

#### Guest Users

Authorization checks within gates and policies return `false` by default whenever an incoming HTTP request originates from an unauthenticated user. To enable these checks to process unauthenticated requests instead, you can define the user argument with a `None` default value or specify a `None` or `Optional` type-hint:

```python title="app/policies/post.py"
--8<-- "docs_src/security/authorization/guest_users_example.py"
```

#### Policy Filters

If you need to grant a user permission for every action controlled by a policy, you can implement a `before` method. Because this method runs prior to any other policy checks, it allows you to approve access in advance. This approach is typically used to give application administrators unrestricted access:

```python title="app/policies/post.py"
--8<-- "docs_src/security/authorization/policy_filters_example.py"
```

Returning `false` from the `before` method will deny all authorization checks for a specific type of user.
Alternatively, returning `None` allows the authorization evaluation to proceed to the corresponding policy method.

!!! warning "`before` Method Logic"
    The `before` method of a policy class is executed only if a method matching the name of the ability being checked is defined within that class.

### Authorizing Actions {: #authorizing-actions--policies}

#### Using the User Model

The `User` model provided with your *Pyrannic* application features two useful authorization methods: `can` and `cannot`. Both methods accept two arguments: the action you want to authorize and the associated model.

For instance, let's check if a user has permission to update a specific `Post` model using these methods. This could be implemented inside a router function:

```python title="app/http/routers/posts.py" hl_lines="32 33"
--8<-- "docs_src/security/authorization/authorizing_actions_example_04.py"
```

When a [policy is registered](#registering-policies) for the specified model, the `can` method automatically executes it and returns a boolean result. Otherwise, if no policy exists for that model, the method attempts to invoke a closure-based `Gate` corresponding to the action name.

#### Using the Gate Interface

##### The *authorize* Method

Beyond the methods available on the `User` model, actions can also be authorized using the `authorize` method on the Gate interface.

Similar to the `can` method, it requires the action name and the target model. Should authorization fail, the `authorize` method raises a `ForbiddenException`, which the Pyrannic exception handler automatically translates into an HTTP 403 response:

```python title="app/http/routers/posts.py" hl_lines="31"
--8<-- "docs_src/security/authorization/authorizing_actions_example_05.py"
```

##### The rest of Methods

The remaining methods of the `Gate` interface that we alredy saw when [using abilities](#authorizing-actions--abilities) (`allows`, `denies`, `check`, `any`, `none`, `can`, `cannot`) can be also used to authorize actions with policies:

```python title="app/http/routers/posts.py"
--8<-- "docs_src/security/authorization/authorizing_actions_example_06.py"
```

#### Using the Gate Facade

!!! danger "Work in Progress"
    This section is currently under development and will be accessible very soon.

#### Actions without a Required Model

Certain policy methods, such as `create`, do not require a specific model instance. When authorizing these actions, you must supply a model class `type` instead. This model class `type` is then evaluated to instantiate the appropriate policy to execute when authorizing the action:

```python title="app/http/routers/posts.py"
--8<-- "docs_src/security/authorization/authorizing_actions_example_07.py"
```

#### Supplying Additional Context

!!! danger "Work in Progress"
    This section is currently under development and will be accessible very soon.
