from app.contracts import MyDependencyInterface

from pyrannic.ioc import Resolves, singleton


@singleton
class SnowflakeService:
    # You could type-hint dependencies in your container resolution callback
    async def __ioc_resolved__(
        self, my_dependency: Resolves[MyDependencyInterface]
    ) -> None:
        """
        Perform here any task that you want to run once the container resolves this dependency.
        """
