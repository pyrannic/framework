sql = query_builder.distinct().select("first_name").from_("users").to_sql()
print(sql)  # SELECT DISTINCT "first_name" FROM "users"
