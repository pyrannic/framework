## Why Pyrannic?

Pyrannic aims to be a comprehensive web framework that handles the complexities of application development, allowing you to focus on building great software while the framework manages the underlying details.

To accelerate your development process, Pyrannic introduces abstraction layers over tools like FastAPI, Pydantic, and SQLAlchemy. Key features include:

- Default SQLAlchemy implementations for [models](orm/models.md) and [repositories](orm/repositories.md) interfaces.
- REST [Resources](resources.md) and [collections](collections.md) built upon Pydantic by default.
- Specialized [service providers](service-providers.md) for [routers](routers.md) and [middlewares](middlewares.md) that offer a structured approach to application design.

Ultimately, the choice is yours. Pyrannic is designed to be opinionated yet flexible:

- If you prefer not to use SQLAlchemy, you can implement your own ORM interfaces, such as `QueryBuilderInterface` or `RepositoryInterface`.
- If the provided router or middleware logic doesn't suit your project, you can create a [custom service provider](routers.md#custom-service-provider) to manage them your way.

While Pyrannic provides a clear path forward, it remains committed to giving you the freedom to choose your own tools and structures.

## Creating a Pyrannic Application

After you have installed *Python*, *pip* and create and activate a [virtual environment](https://fastapi.tiangolo.com/virtual-environments/) you're ready to create a new Pyrannic application. You can install it running the next *pip* command:

```bash
pip install pyrannic
```

Now, you can scaffold the initial Pyrannic application with the next Pyrannic CLI command:

```bash
pyrannic new
```

This will create the folder's structure of a Pyarannic application in your execution folder.

!!! abstract "Initial application"
    The initial application that you have created is based in the code that you can find in this repository: [https://github.com/pyrannic/application](https://github.com/pyrannic/application)

## Initial Configuration

Pyrannic stores all configuration files within the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you.

Pyrannic is ready for development immediately with virtually no extra setup. However, you might want to examine the `config/app.py` file. Its documentation details several customizable parameters, including `name` and `locale`, which you can adjust to suit your specific application needs.

### Environment Based Configuration

Pyrannic utilizes a `.env` file located at the application's root to manage configuration values that often differ between local development environments and production servers.

To maintain security and accommodate environment-specific needs, this file should be excluded from source control. Committing the `.env` file poses a significant risk, as it could expose sensitive credentials to unauthorized individuals who gain access to the repository.

!!! abstract "Know More"
    For more information about the `.env` file and environment based configuration, check out the full [configuration documentation](configuration.md).

### Databases and Migrations

After setting up your Pyrannic application, your next step will likely involve database storage. Pyrannic is configured to use an SQLite database out of the box, as defined in your `.env` file. And also, it automatically generated a `database/database.sqlite` file during the initial setup.

If you prefer to use another database driver such as MySQL or PostgreSQL, you can update your .env configuration file to use the appropriate database. For example, if you wish to use MySQL, update your .env configuration file's DB_* variables like so:


You can modify your `.env` configuration file to use a different database driver, such as MySQL or PostgreSQL, by updating the relevant database settings. For example, if you decide to switch to MySQL, you should adjust the `DB_*` variables in your `.env` file as follows:

```bash
DB_CONNECTION="mysql"
DB_HOST="localhost"
DB_PORT=3306
DB_DATABASE="pyrannic"
DB_USERNAME="root"
DB_PASSWORD=
```

!!! abstract "Know More"
    For more information about how the database migrations work in Pyrannic, check out the full [migrations documentation](database/migrations.md).

## Next Steps

With your Pyrannic application now established, you might be considering your next learning objectives. To begin, we highly suggest gaining a solid understanding of Pyrannic's inner workings by reviewing the documentation listed below:

- [Configuration](configuration.md)
- [Directory Structure](directory-structure.md)
- [IoC Container](ioc-container.md)
- [Bootstrap](bootstrap.md)
- [Service Providers](service-providers.md)