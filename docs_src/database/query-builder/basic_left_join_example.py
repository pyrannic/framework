sql = (
    query_builder
    .from_("users")
    .left_join("posts", "users.id", "=", "posts.user_id")
    .to_sql()
)

print(sql)
# SELECT *
# FROM "users"
# LEFT JOIN "posts" ON "users"."id" = "posts"."user_id"
