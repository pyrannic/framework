sql = query_builder.from_("posts").order_by("published_at").first().to_sql()

print(sql)  # SELECT * FROM "posts" ORDER BY "published_at" DESC LIMIT 1
