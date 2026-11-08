sql = query_builder.from_("posts").offset(50).limit(25).to_sql()

print(sql)  # SELECT * FROM "posts" OFFSET 50 LIMIT 25
