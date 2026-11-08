sql = query_builder.from_("posts").latest("published_at").first().to_sql()

print(sql)  # SELECT * FROM "posts" ORDER BY "published_at" DESC LIMIT 1
