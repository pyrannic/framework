sql = query_builder.from_("posts").to_sql()
print(sql)  # SELECT * FROM "posts"
