### 11. DELETE 与 UPDATE...SET...
当涉及到数据库操作时，DELETE和UPDATE是两个常用的命令。
<span style="color:pink">DELETE命令用于从数据库表中删除一条或多条记录。</span>它可以根据指定的条件删除符合条件的记录，也可以删除整个表中的所有记录。
以下是一个示例，演示如何使用DELETE命令删除符合特定条件的记录：
```sql
DELETE FROM 表名
WHERE 条件;
```
例如，假设我们有一个名为"students"的表，其中包含学生的信息。我们想要删除名字为"John"的学生记录，可以使用以下命令：
```sql
DELETE FROM students
WHERE name = 'John';
```
<span style="color:pink">UPDATE...SET...命令用于更新数据库表中的记录。</span>它可以根据指定的条件更新符合条件的记录的值。
以下是一个示例，演示如何使用UPDATE命令更新符合特定条件的记录：
```sql
UPDATE 表名
SET 列名 = 新值
WHERE 条件;
```
例如，假设我们有一个名为"students"的表，其中包含学生的信息。我们想要将名字为"John"的学生的年龄更新为20岁，可以使用以下命令：
```sql
UPDATE students
SET age = 20
WHERE name = 'John';
```
这将把名字为"John"的学生的年龄更新为20岁。
请注意，DELETE和UPDATE命令都是非常强大的，因此在使用它们时要小心，确保你了解操作的影响，并且在执行之前备份重要的数据。