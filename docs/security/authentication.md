## Introduction

Pyrannic's authentication system is fundamentally structured around two core components: "guards" and "user providers."

[Guards](#guards) specify the way users are authenticated for every request. For example, Pyrannic includes a bearer guard out of the box, which utilizes HTTPBearer from FastAPI.

[User Providers](#user-providers) determine how users are retrieved from your persistent storage. While Pyrannic offers built-in support for retrieving users through its ORM backed by SQLAlchemy, you have the flexibility to implement custom providers to suit your application's requirements.

Your application's authentication configuration file is located at `config/auth.php`. Inside, you will find several well-documented options for customizing the behavior of Pyrannic's authentication services.

## Authentication Quickstart

### Securing Routes

To secure your routes, you need to use the `Authenticate` dependency. Depending on the granularity of access control required for your application, you can secure an entire router instance:

```python hl_lines="8"
--8<-- "docs_src/security/authenticate_router_example.py"
```

Or individual routes:

```python hl_lines="8"
--8<-- "docs_src/security/authenticate_router_example.py"
```

This dependency handles the authentication workflow by leveraging the configured **guard** and **user provider**.

- Guard determines how credentials and request tokens are inspected and validated for each incoming request.
- User Provider fetches and retrieves the user record from the underlying storage or database based on the validated credentials.

When a request hits a protected route, the `Authenticate` dependency automatically executes these checks before allowing the request handler to proceed. If authentication succeeds, the authenticated user context is attached to the request; otherwise, an unauthorized error response is returned.

### Retrieving the Authenticated User

!!! danger "Work in Progress"
    This section is currently under development.

### Config

In the application's authentication configuration file located at `config/auth.php`, you will find the main settings required to specify which authentication guard and corresponding user provider the system should utilize. By default, Pyrannic comes pre-configured with an HTTP Bearer token-based guard, which integrates directly with FastAPI's HTTPBearer security model. For user management and persistence, it defaults to a User Provider driven by its ORM layer, backed by SQLAlchemy.

!!! danger "Work in Progress"
    This section is currently under development.

## Guards

For every incoming request, the guard defines the comprehensive process used to inspect, verify, and validate incoming user credentials and request tokens. This validation mechanism ensures that access is strictly limited to authorized users and clients while maintaining the overall integrity and safety of backend resources.

!!! danger "Work in Progress"
    This section is currently under development.

    - Inject the guard example.

### The Guard Interface


## User Providers

### The User Provider Interface
### The Authenticatable Interface

!!! danger "Work in Progress"
    This section is currently under development and will be accessible very soon.
