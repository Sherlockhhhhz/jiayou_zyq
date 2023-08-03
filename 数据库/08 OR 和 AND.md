### 8. OR 和 AND
在MySQL中，"OR"是一个逻辑运算符，用于在查询条件中指定多个条件之一成立即可返回结果。以下是使用"OR"运算符的代码示例：
```sql
SELECT * FROM students WHERE age = 20 OR age = 22;
```
上述代码将返回年龄为20或22的学生记录。
```sql
SELECT * FROM students WHERE name = 'John' OR name = 'Jane';
```
上述代码将返回名字为"John"或"Jane"的学生记录。
你还可以将"OR"运算符与其他比较运算符结合使用，以构建更复杂的查询条件。例如：
```sql
SELECT * FROM students WHERE age > 18 OR (name = 'John' AND gender = 'Male');
```
上述代码将返回年龄大于18岁或者名字为"John"且性别为"Male"的学生记录。
请注意，在使用"OR"运算符时，要注意逻辑关系和括号的使用，以确保查询条件的正确性和预期结果。
在MySQL中，"AND"是一个逻辑运算符，用于在查询条件中指定多个条件同时成立才返回结果。以下是使用"AND"运算符的代码示例：
```sql
SELECT * FROM students WHERE age = 20 AND gender = 'Male';
```
上述代码将返回年龄为20且性别为"Male"的学生记录。
```sql
SELECT * FROM students WHERE name = 'John' AND grade = 'A';
```
上述代码将返回名字为"John"且成绩为"A"的学生记录。
你还可以将"AND"运算符与其他比较运算符结合使用，以构建更复杂的查询条件。例如：
```sql
SELECT * FROM students WHERE age > 18 AND grade = 'A' AND gender = 'Female';
```
上述代码将返回年龄大于18岁且成绩为"A"且性别为"Female"的学生记录。
请注意，在使用"AND"运算符时，要注意逻辑关系和括号的使用，以确保查询条件的正确性和预期结果。