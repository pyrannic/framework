## Introduction

The default Pyrannic application structure is intended to provide a great starting point for both large and small applications.

Excepting the `app` directory, the other root directories are intended to be used by Pyrannic mainly.

## The Root Directory

### The `main.py` File

This is the entrypoint of your application. In a fresh Pyrannic application, this file contains the creation of the application and serves it using `uvicorn`.

### The `app` Directory

The `app` directory contains the core code of your application. We'll explore this directory in more detail soon; however, almost all of the code in your application will be in this directory.

### The `bootstrap` Directory

The `bootstrap` directory contains the `providers.py`, `routers.py`, and `middlewares.py` files which configure the bootstrapping of the framework.

### The `config` Directory

The `config` directory, as the name implies, contains all of your application's configuration files. It's a great idea to read through all of these files and familiarize yourself with all of the options available to you.

### The `database` Directory

The `database` directory contains your database migrations. If you wish, you may also use this directory to hold an SQLite database.

## The App Directory

### The `http` Directory

The `http` directory contains your `routers`, `middlewares`, `requests` and `resources`. Almost all of the logic to handle requests entering your application will be placed in this directory.

### The `models` Directory

The `models` directory contains all of your database model classes. The ORM included with Pyrannic provides a simple ActiveRecord implementation for working with your database. Each database table has a corresponding "Model" which is used to interact with that table.

### The `providers` Directory

The `providers` directory contains all of the [service providers](service-providers.md) for your application. Service providers bootstrap your application by binding services in the [IoC Container](ioc-container.md), registering events, or performing any other tasks to prepare your application for incoming requests.

In a fresh Pyrannic application, this directory will already contain the `AppServiceProvider`. You are free to add your own providers to this directory as needed.

### The `repositories` Directory

The `repositories` directory contains all of your database repository classes. The ORM included with Pyrannic provides a simple QueryBuilder implementation for working with your database. Each database table has a corresponding "Repository" which is used to interact with that table. Repositories allow you to query for data in your tables, as well as insert new records into the table.
