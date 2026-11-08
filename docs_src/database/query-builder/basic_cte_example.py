order_details_query = (
    query_builder
    .from_("orders as o")
    .select("o.order_id", "c.full_name", "p.price", "o.quantity", "o.created_at")
    .join("customers as c", "c.customer_id", "=", "o.customer_id")
    .join("products as p", "p.product_id", "=", "o.product_id")
    .to_sql()
)

sql = (
    query_builder
    .with_query("order_details", order_details_query)
    .select(
        "full_name",
        query_builder.raw("price * quantity as total"),
    )
    .from_("order_details")
    .group_by("full_name")
    .having(query_builder.raw("total > 1000"))
    .to_sql()
)

print(sql)

# WITH "order_details" AS (
#   SELECT "o.order_id", "c.full_name", "p.price", "o.quantity", "o.created_at"
#   FROM "orders" AS "o"
#   JOIN "customers" AS "c" ON "c.customer_id" = "o.customer_id"
#   JOIN "products" AS "p" ON "p.product_id" = "o.product_id"
# )
# SELECT "full_name", price * quantity as total
# FROM "order_details"
# GROUP BY "full_name"
# HAVING total > 1000
