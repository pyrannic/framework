## Introduction

Complementing its built-in [authentication](/security/authentication) services, Pyrannic offers a structured and simple way to manage authorization checks, enabling you to easily validate user actions against specific resources. For instance, an authenticated user might still lack the permissions required to modify or remove specific database records or models within your application. To handle these validation requirements smoothly, Pyrannic delivers an organized and simple approach to managing authorization checks.

Pyrannic offers two main mechanisms for authorizing actions: [gates](#gates) and [policies](#policies). Gates deliver a straightforward, closure-based method for authorization. In contrast, policies organize authorization logic around a specific model or resource. This documentation will first explain gates before moving on to examine policies.

!!! abstract "Gates vs. Policies"
    Applications can use a combination of both gates and policies. Gates are best suited for actions that are not related to any specific model or resource (such as viewing an admin panel), while policies should be used to authorize actions for a particular model or resource.


# Gates

!!! danger "Work in Progress"
    This section is currently under development and will be accessible very soon.

# Policies

!!! danger "Work in Progress"
    This section is currently under development and will be accessible very soon.
