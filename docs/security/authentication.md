## Introduction

Pyrannic's authentication system is fundamentally structured around two core components: "guards" and "user providers."

[Guards](#guards) specify the way users are authenticated for every request. For example, Pyrannic includes a bearer guard out of the box, which utilizes HTTPBearer from FastAPI.

[User Providers](#user-providers) determine how users are retrieved from your persistent storage. While Pyrannic offers built-in support for retrieving users through its ORM backed by SQLAlchemy, you have the flexibility to implement custom providers to suit your application's requirements.

!!! tip "Safeguard"
    While Guards and User Providers provide everything you need to protect your application's routes, they won't take advantage of the automatically generated documentation provided by FastAPI, so you won't be able to display the "lock" feature.

    To try to fix this lack, you have at your disposal the [Safeguard](#safeguard) dependency. You can check its documentation below.

## Config

!!! danger "Work in Progress"
    This section is currently under development and will be accessible very soon.

## Guards

!!! danger "Work in Progress"
    This section is currently under development and will be accessible very soon.

## User Providers

!!! danger "Work in Progress"
    This section is currently under development and will be accessible very soon.

## Safeguard

!!! danger "Work in Progress"
    This section is currently under development and will be accessible very soon.
