sql = query_builder.add_select("user_id as author_id").to_sql()
print(sql)
# SELECT
#   "id",
#   "title",
#   "created_at" AS "published_at",
#   "user_id" AS "author_id"
# FROM "posts"
