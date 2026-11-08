sql = query_builder.from_("posts").oldest("published_at").first().to_sql()

print(sql)  # SELECT * FROM "posts" ORDER BY "published_at" ASC LIMIT 1
