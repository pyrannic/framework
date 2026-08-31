## Introduction

*Pyrannic*'s authentication system is fundamentally structured around two core components: "guards" and "user providers."

[Guards](#guards) specify the way users are authenticated for every request. For example, *Pyrannic* includes a `BearerGuard`  and a `JwtGuard` out of the box, which utilizes `HTTPBearer` from *FastAPI*.

[User Providers](#user-providers) determine how users are retrieved from your persistent storage. While *Pyrannic* offers built-in support for retrieving users through its ORM backed by *SQLAlchemy*, you have the flexibility to implement custom providers to suit your application's requirements.

Your application's authentication configuration file is located at `config/auth.py`. Inside, you will find several well-documented options for customizing the behavior of *Pyrannic*'s authentication services.

## Securing Routes

To secure your routes, you need to use the `Authenticate` dependency. Depending on the granularity of access control required for your application, you can secure an entire router instance:

```python hl_lines="8"
--8<-- "docs_src/security/authentication/securing_routes_example_01.py"
```

Or individual routes:

```python hl_lines="8"
--8<-- "docs_src/security/authentication/securing_routes_example_02.py"
```

This dependency handles the authentication workflow by leveraging the configured **guard** and **user provider**.

- Guard determines how credentials and request tokens are inspected and validated for each incoming request.
- User Provider fetches and retrieves the user record from the underlying storage or database based on the validated credentials.

When a request hits a protected route, the `Authenticate` dependency automatically executes these checks before allowing the request handler to proceed. If authentication succeeds, the authenticated user context is attached to the `Guard`; otherwise, an unauthorized error response is returned.

### Allowing Guest Users

If authentication fails, the `Authenticate` dependency returns an unauthorized error response, as previously noted.

In certain scenarios, it may be desirable to grant access to both authenticated users and guests for the same endpoint. In such cases, set the `allow_guests` parameter of the `Authenticate` dependency to `True`:

```python hl_lines="8"
--8<-- "docs_src/security/authentication/securing_routes_example_03.py"
```

### Checking if the Current User is Authenticated

You can verify whether an incoming HTTP request is from an authenticated user by calling the `check` method on the `Guard` interface. If the user is authenticated, this method returns `True`:

```python hl_lines="12 15"
--8<-- "docs_src/security/authentication/securing_routes_example_04.py"
```

## Fetching the Authenticated User

### The `user` Property

When handling incoming requests, interacting with the currently authenticated user is a common task. You can retrieve this user directly through the `user` property provided by the `Guard` interface:

```python title="app/http/routers/posts.py" hl_lines="15 17 18"
--8<-- "docs_src/security/authentication/fetching_auth_user_example_01.py"
```

### The `maybe_user` Property

The `user` property raises a `ValueError` exception when no authenticated user is present in the incoming HTTP request.
To retrieve the user without triggering an exception, use the `maybe_user` property instead. This property returns the authenticated user or `None` if no authenticated user exists:

```python title="app/http/routers/posts.py" hl_lines="15 17 18"
--8<-- "docs_src/security/authentication/fetching_auth_user_example_02.py"
```

### The `id` and `maybe_id` Properties

If you just need to access to the identifier of the authenticated user there are two useful methods for that.
The `id` property is the counterpart for the `user` property returning the identifier of the authenticated user,
and throwing a `ValueError` exception if there is not such authenticated user. In the other hand, you have `maybe_id``
which allow you to fetch the identifier of the user or `None` in the case that there is not an authenticated user:

```python
--8<-- "docs_src/security/authentication/fetching_auth_user_example_03.py"
```

## Guards

For every incoming request, the guard defines the comprehensive process used to inspect, verify, and validate incoming user credentials and request tokens. This validation mechanism ensures that access is strictly limited to authorized users and clients while maintaining the overall integrity and safety of backend resources.

Built upon *FastAPI*'s `HTTPBearer` security model, *Pyrannic* includes two built-in *Guards*: `BearerGuard` and `JwtGuard`.

### Configure the Guard to Use

In the application's authentication configuration file located at `config/auth.py`, you will find the main settings required to specify which authentication guard the system should utilize. By default, *Pyrannic* comes pre-configured to use the `BearerGuard`:

```python title="config/auth.py" hl_lines="7"
--8<-- "docs_src/security/authentication/guards_example_01.py"
```

To change the guard, update the setting directly in your `config/auth.py` file or set the corresponding environment variable:

```bash title=".env" hl_lines="7"
--8<-- "docs_src/security/authentication/guards_example_02.env"
```

### The Guard Interface

If you need it, you can create your own *guard* implementing the [`GuardInterface`](https://github.com/pyrannic/framework/blob/main/pyrannic/contracts/auth/guard.py):

```python title="app/auth/my_awesome_guard.py"
--8<-- "docs_src/security/authentication/guard_interface_example_01.py"
```

After create your *guard* you need to register it in the IoC container in some of your service providers:

```python title="app/providers/app.py" hl_lines="9"
--8<-- "docs_src/security/authentication/guard_interface_example_02.py"
```

## User Providers

### The User Provider Interface

!!! danger "Work in Progress"
    This section is currently under development and will be accessible very soon.

### The Authenticatable Interface

Having reviewed each method on the `UserProvider,` let's turn our attention to the `Authenticatable` contract.
Keep in mind that user providers are expected to return implementations of this interface through
the `retrieveById`, `retrieveByToken`, and `retrieveByCredentials` methods:

```python title="pyrannic/contracts/auth/authenticatable.py"
--8<-- "docs_src/security/authentication/authenticatable_interface_example_01.py"
```

This interface is straightforward. The `get_auth_identifier_name` method must return the name of the primary key column for the user, whereas the `get_auth_identifier` method must return the user's primary key value. In a SQL database backend, this typically corresponds to the auto-incrementing primary key assigned to the user record. Furthermore, the `get_auth_password_name` method must return the name of the password column, and the `get_auth_password` method must return the user's hashed password.

By utilizing this interface, the authentication system can seamlessly integrate with any "user" class, independent of your chosen *ORM* or storage abstraction layer.
