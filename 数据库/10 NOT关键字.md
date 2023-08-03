### 10. NOT
在MySQL中，"NOT"是一个逻辑运算符，用于取反查询条件的结果。它可以与其他关键字（如"LIKE"、"IN"、"BETWEEN"等）一起使用，以排除满足特定条件的数据。以下是"NOT"关键字的介绍和代码示例：
1. NOT关键字用于取反查询条件的结果。
   例子：
   ```sql
   SELECT * FROM students WHERE NOT age = 20;
   ```
   上述代码将返回年龄不等于20的学生记录。
2. NOT可以与其他关键字一起使用，例如NOT LIKE、NOT IN、NOT BETWEEN等。
   例子：
   ```sql
   SELECT * FROM students WHERE NOT name LIKE 'J%';
   ```
   上述代码将返回名字不以字母"J"开头的学生记录。
3. NOT还可以与其他逻辑运算符（如AND、OR）结合使用，以构建更复杂的查询条件。
   例子：
   ```sql
   SELECT * FROM students WHERE NOT (age = 20 AND gender = 'Male');
   ```
   上述代码将返回年龄不等于20或者性别不为"Male"的学生记录。
请注意，在使用"NOT"关键字时，要注意逻辑关系和括号的使用，以确保查询条件的正确性和预期结果。

以下是一个综合示例：

```sql
SELECT * FROM students WHERE NOT (age = 20 OR gender = 'Male');
```
上述代码将返回年龄不等于20且性别不为"Male"的学生记录。
