from pyrannic.contracts.database import QueryBuilderInterface
from pyrannic.database import Grammar, QueryBuilder


def test_before_query_callbacks():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    def callback(qb: QueryBuilderInterface):
        qb.where("id", "=", 1)

    query_builder.before_query(callback).select("name").from_("users")

    sql = query_builder.to_sql()
    assert sql == 'SELECT "name" FROM "users" WHERE "id" = %s'
