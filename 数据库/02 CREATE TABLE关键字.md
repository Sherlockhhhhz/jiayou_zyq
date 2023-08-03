### 2. CREATE TABLE语关键字  
`CREATE TABLE`语句用于在数据库中创建一个新的表。它定义了表的结构，包括表名、列名、数据类型和约束等。
`CREATE TABLE`语句的基本语法如下：

```sql
CREATE TABLE table_name (
    column1 datatype constraint,
    column2 datatype constraint,
    ...
    columnN datatype constraint
);
```
其中，`table_name`是要创建的表的名称，`column1`、`column2`等是表的列名，`datatype`是列的数据类型，`constraint`是列的约束条件(比如NULL, NOT NULL, PRIMARY KEY等)。
以下是一个示例，创建一个名为`users`的表，包含`id`、`name`和`age`三个列：

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT
);
```
在上面的示例中，`id`列被定义为主键（`PRIMARY KEY`），`name`列被定义为不允许为空（`NOT NULL`），`age`列没有定义任何约束。
你可以根据需要在`CREATE TABLE`语句中添加其他约束，如唯一性约束、外键约束等。此外，你还可以在列定义中指定默认值、自动递增等属性。
请注意，<span style="color:pink;">`CREATE TABLE`语句只能在数据库中创建新表，如果表已经存在，将会出现错误。</span>