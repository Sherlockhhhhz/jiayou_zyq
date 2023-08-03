### 19. LIMIT 关键字
LIMIT是一个在SQL中常用的关键字，用于限制查询结果的返回行数。它可以用于SELECT语句中，以便只返回满足条件的前几行。

LIMIT关键字的语法如下：
```
SELECT column1, column2, ...
FROM table_name
WHERE condition
LIMIT number_of_rows;
```
其中，column1, column2, ...是要查询的列名，table_name是要查询的表名，condition是可选的筛选条件，number_of_rows是要返回的行数。

使用LIMIT关键字后，查询结果将被限制为指定的行数。可以通过指定一个整数值来控制返回的行数。

以下是一个示例：
假设有一个名为"customers"的表，其中包含"customer_id"和"customer_name"两列。如果我们只想返回前5个顾客的信息，可以使用以下查询：
```
SELECT customer_id, customer_name
FROM customers
LIMIT 5;
```
这将返回"customers"表中前5个顾客的customer_id和customer_name。

LIMIT关键字在需要限制结果集大小时非常有用，可以帮助我们控制查询结果的数量，以便更有效地处理数据。