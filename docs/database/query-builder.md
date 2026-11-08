## Introduction

Pyrannic's database query builder offers an intuitive and fluent interface for constructing database queries. Compatible with all supported Pyrannic database systems, it seamlessly handles the majority of your application's database operations.

To safeguard your application from SQL injection vulnerabilities, the query builder utilizes database connection parameter binding. Consequently, strings supplied as query bindings do not require manual sanitization or cleaning.

## Selects and Froms Methods

### `from_`

You can specify which table to use using the `from_` method:

```python
--8<-- "docs_src/database/query-builder/basic_from_example.py"
```

As you can see above, by default, if you don't specify the columns to select, `*` will be used to select all of them.

### `select`

When retrieving data from a database table, you might not always need every column. You can define a custom select clause for your query by utilizing the `select` method:

```python
--8<-- "docs_src/database/query-builder/basic_select_example.py"
```

#### `add_select`

To append a column to an existing select clause on a query builder instance, use the `add_select` method.

```python
--8<-- "docs_src/database/query-builder/basic_add_select_example.py"
```

### `distintc`

By using the `distinct` method, you can force the query to produce unique results:

```python
--8<-- "docs_src/database/query-builder/basic_distinct_example.py"
```

## Joins Methods

### `join`

You can use the query builder to include join clauses within your queries.
To execute a standard inner join, call the `join` method on a query builder instance.
The initial argument supplied to the `join` method designates the target table for the join,
whereas the subsequent arguments define the column constraints.
Additionally, you can link multiple tables within a single query:

```python
--8<-- "docs_src/database/query-builder/basic_join_example.py"
```

### `left_join`

To execute a "left join" rather than an "inner join", utilize the `left_join` method.
The signature for this method is identical to that of the `join` method:

```python
--8<-- "docs_src/database/query-builder/basic_left_join_example.py"
```

### `right_join`

!!! danger "Work in Progress"
    The `right_join` is currently under development and will be available very soon.

In the same way, to execute a "right join" rather than an "inner join", utilize the `right_join` method.
The signature for this method is identical to that of the `join` or `left_join` methods:

```python
--8<-- "docs_src/database/query-builder/basic_right_join_example.py"
```

### `cross_join`

!!! danger "Work in Progress"
    The `cross_join` is currently under development and will be available very soon.

To execute a "cross join", you can utilize the `cross_join` method.
This creates a Cartesian product by combining the initial table with the joined table:

```python
--8<-- "docs_src/database/query-builder/basic_cross_join_example.py"
```

## Unions Methods

### `union`

!!! danger "Work in Progress"
    This is currently under development and will be accessible very soon.

### `union_all`

!!! danger "Work in Progress"
    This is currently under development and will be accessible very soon.

## Wheres

## Ordering

### The `order_by` Method

You can sort query results by a specified column using the `order_by` method.
This method accepts two arguments:

- The target column to sort by as first argument.
- The sort direction, which can be either `SortDirection.ASC` or `SortDirection.DESC`, as second argument.

```python
--8<-- "docs_src/database/query-builder/basic_order_by_example.py"
```

### The `latest` and `oldest` Methods

You can easily order results by date using the `latest` and `oldest` methods.
Results are sorted by the table's `created_at` column by default, though you can also specify a column name to sort by:

```python
--8<-- "docs_src/database/query-builder/basic_latest_example.py"
```

## Grouping

### The `group_by` and `having` Methods

The `group_by` and `having` methods allow you to group query results.
Additionally, the `having` method shares a similar signature to the where method:

!!! danger "Work in Progress"
    This is currently under development and will be accessible very soon.

## Limit & Offset

To control your query results, you can use the following methods:

- `limit`: Restricts the total number of returned results.
- `offset`: Skips a specified number of initial results.

```python
--8<-- "docs_src/database/query-builder/basic_limit_offset_example.py"
```

## Common Tables Expressions (CTEs)

### The `with_query` Method

Use the `with_query` method to define Common Table Expressions (CTEs) and keep complex queries modular and readable.

```python
--8<-- "docs_src/database/query-builder/basic_cte_example.py"
```

## Inserts

## Updates

## Deletes