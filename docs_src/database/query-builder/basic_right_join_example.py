sql = (
    query_builder
    .from_("users")
    .right_join("posts", "users.id", "=", "posts.user_id")
    .to_sql()
)

print(sql)
# SELECT *
# FROM "users"
# RIGHT JOIN "posts" ON "users"."id" = "posts"."user_id"
