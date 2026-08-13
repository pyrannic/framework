from pyrannic.container.decorators import scoped
from pyrannic.orm.sqlalchemy.repository import Repository
from tests.application.app.models.post import Post


@scoped
class PostsRepository(Repository[Post]):
    pass
