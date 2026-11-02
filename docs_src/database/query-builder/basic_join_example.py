sql = (
    query_builder
    .from_("users")
    .join("posts", "users.id", "=", "posts.user_id")
    .join("comments", "posts.id", "=", "comments.post_id")
    .select("users.first_name as author", "posts.title", "comments.body")
    .to_sql()
)

print(sql)
# SELECT
#   "users"."first_name" AS "author",
#   "posts"."title",
#   "comments"."body"
# FROM "users"
# JOIN "posts" ON "users"."id" = "posts"."user_id"
# JOIN "comments" ON "posts"."id" = "comments"."post_id"
