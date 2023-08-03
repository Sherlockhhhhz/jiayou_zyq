### 5. SELECT 语句
`SELECT`语句用于从数据库中检索数据。它允许你指定要检索的表名、列名、条件和排序等。

`SELECT`语句的基本语法如下：

```sql
SELECT column1, column2, ..., columnN
FROM table_name
WHERE condition
ORDER BY column_name [ASC|DESC];
```
其中，`column1, column2, ..., columnN`是要检索的列名，可以使用通配符`*`表示检索所有列。`table_name`是要检索数据的表名。`WHERE`子句用于指定检索的条件，可以根据需要使用比较运算符、逻辑运算符和函数等。`ORDER BY`子句用于指定结果的排序方式，可以按照一个或多个列进行升序（`ASC`）或降序（`DESC`）排序。
以下是一个示例，从名为`users`的表中检索`name`和`age`列的数据：
```sql
SELECT name, age
FROM users;
```
在上面的示例中，我们从`users`表中检索了`name`和`age`列的数据。
你可以根据需要添加`WHERE`子句来指定检索的条件，例如：
```sql
SELECT name, age
FROM users
WHERE age > 25;
```
上述示例将检索`age`大于25的用户的`name`和`age`列数据。
请注意，`SELECT`语句可以使用多种其他功能，如聚合函数（如`COUNT`、`SUM`、`AVG`等）、连接操作（如`JOIN`）、分组（`GROUP BY`）等，以满足更复杂的数据检索需求。