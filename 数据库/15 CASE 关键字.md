### 15. CASE 关键字
CASE关键字是在SQL中用于实现条件逻辑的关键字。它允许根据条件对结果进行分支处理，类似于编程语言中的if-else语句。

CASE关键字有两种形式：简单CASE表达式和搜索CASE表达式。

1. 简单CASE表达式：
   简单CASE表达式用于对单个表达式进行比较，并根据不同的比较结果执行相应的操作。

   示例：
   ```sql
   SELECT column_name,
       CASE expression
           WHEN value1 THEN result1
           WHEN value2 THEN result2
           ...
           ELSE result
       END
   FROM table_name;
   ```

   示例说明：
   ```sql
   SELECT name,
       CASE grade
           WHEN 'A' THEN '优秀'
           WHEN 'B' THEN '良好'
           WHEN 'C' THEN '及格'
           ELSE '不及格'
       END
   FROM students;
   ```

2. 搜索CASE表达式：
   搜索CASE表达式用于根据多个条件进行比较，并根据满足条件的结果执行相应的操作。

   示例：
   ```sql
   SELECT column_name,
       CASE
           WHEN condition1 THEN result1
           WHEN condition2 THEN result2
           ...
           ELSE result
       END
   FROM table_name;
   ```

   示例说明：
   ```SQL
   SELECT name,
       CASE
           WHEN score >= 90 THEN '优秀'
           WHEN score >= 80 THEN '良好'
           WHEN score >= 60 THEN '及格'
           ELSE '不及格'
       END
   FROM students;
   ```

CASE关键字在SQL中非常有用，可以根据不同的条件进行灵活的数据处理和结果返回。它可以用于SELECT语句、UPDATE语句、INSERT语句等各种SQL操作中。