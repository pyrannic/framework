from logging import Logger
from typing import Annotated

from pyrannic.container.param_functions import Resolves
from pyrannic.contracts.orm.repository import T
from pyrannic.orm.sqlalchemy.abstract_query_builder import AbstractQueryBuilder
from pyrannic.orm.sqlalchemy.session import Session


class QueryBuilder(AbstractQueryBuilder[T]):
    def __init__(self, session: Session, logger: Annotated[Logger, Resolves()]):
        self._session = session
        super().__init__(logger=logger)

    @property
    def session(self) -> Session:
        return self._session
