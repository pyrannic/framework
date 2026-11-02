sql = (
    query_builder
    .select("id", "title", "created_at as published_at")
    .from_("posts")
    .to_sql()
)
print(sql)  # SELECT "id", "title", "created_at" AS "published_at" FROM "posts"
