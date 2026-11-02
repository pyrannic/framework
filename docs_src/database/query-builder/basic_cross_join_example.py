sql = query_builder.from_("sizes").cross_join("colors").to_sql()
print(sql)  # SELECT * FROM "sizes" CROSS JOIN "colors"
