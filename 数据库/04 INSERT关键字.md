### 4. INSERT 语句
`INSERT`语句用于向数据库表中插入新的行（记录）。它允许你指定要插入的表名、列名和对应的值。
`INSERT`语句的基本语法如下：
```sql
INSERT INTO table_name (column1, column2, ..., columnN)
VALUES (value1, value2, ..., valueN);
```
其中，`table_name`是要插入数据的表名，`column1, column2, ..., columnN`是要插入数据的列名，`value1, value2, ..., valueN`是对应列的值。
以下是一个示例，向名为`users`的表中插入一条新的记录：
```sql
INSERT INTO users (name, age, email)
VALUES ('John Doe', 25, 'johndoe@example.com');
```
在上面的示例中，我们向`users`表中的`name`、`age`和`email`列插入了一条记录，分别对应的值是`'John Doe'`、`25`和`'johndoe@example.com'`。
你可以根据需要插入多条记录，只需在`VALUES`子句中提供相应的值即可。另外，如果你不想指定要插入数据的列名，可以省略`column1, column2, ..., columnN`部分，但是需要确保提供的值的顺序与表中的列顺序一致。
请注意，插入数据时要确保数据的完整性和一致性，遵循表的约束条件和数据类型要求。
