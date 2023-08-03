





### 16. ORDER BY 关键字
ORDER BY关键字是在SQL中用于对查询结果进行排序的关键字。它可以按照指定的列或表达式对结果进行升序或降序排序。

语法：
```sql
SELECT 列名
FROM 表名
ORDER BY 列名 [ASC|DESC];
```

示例：
```sql
SELECT name, age
FROM students
ORDER BY age DESC;
```

示例说明：
以上示例将从"students"表中选择"name"和"age"列，并按照"age"列进行降序排序。结果将按照年龄从高到低的顺序返回。

ORDER BY关键字可以与SELECT语句一起使用，也可以与UPDATE、DELETE等其他SQL操作一起使用。它提供了灵活的排序选项，可以根据需要对结果进行排序。默认情况下，ORDER BY关键字按照升序排序（ASC），如果需要降序排序，可以使用DESC关键字。

### 17. 常用函数
当涉及到MySQL函数时，有许多不同类型的函数可用于处理和操作数据。下面是一些常见的MySQL函数的例子:
1. 字符串函数：

   - CONCAT函数：用于将多个字符串连接在一起。
   
     示例表：
   
     | id | first_name | last_name |
     |----|------------|-----------|
     | 1  | John       | Doe       |
     | 2  | Jane       | Smith     |
   
     ```sql
     SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM table_name;
     ```
   
     结果表：
   
     | full_name     |
     |---------------|
     | John Doe      |
     | Jane Smith    |
   
   - SUBSTRING函数：用于从字符串中提取子字符串。
   
     示例表：
   
     | id | full_name  |
     |----|------------|
     | 1  | John Doe   |
     | 2  | Jane Smith |
   
     ```sql
     SELECT SUBSTRING(full_name, 6) AS last_name FROM table_name;
     ```
   
     结果表：
   
     | last_name |
     |-----------|
     | Doe       |
     | Smith     |
   
   - UPPER函数：用于将字符串转换为大写。
   
     示例表：
   
     | id | name    |
     |----|---------|
     | 1  | john    |
     | 2  | jane    |
   
     ```sql
     SELECT UPPER(name) AS uppercase_name FROM table_name;
     ```
   
     结果表：
   
     | uppercase_name |
     |----------------|
     | JOHN           |
     | JANE           |
   
   - LOWER函数：用于将字符串转换为小写。
   
     示例表：
   
     | id | NAME    |
     |----|---------|
     | 1  | JOHN    |
     | 2  | JANE    |
   
     ```sql
     SELECT LOWER(NAME) AS lowercase_name FROM table_name;
     ```
   
     结果表：
   
     | lowercase_name |
     |----------------|
     | john           |
     | jane           |
   
   - LENGTH函数：用于返回字符串的长度。
   
     示例表：
   
     | id | name   |
     |----|--------|
     | 1  | John   |
     | 2  | Jane   |
   
     ```sql
     SELECT name, LENGTH(name) AS name_length FROM table_name;
     ```
   
     结果表：
   
     | name | name_length |
     |------|-------------|
     | John | 4           |
     | Jane | 4           |
   
   - TRIM函数：用于去除字符串两端的空格。
   
     示例表：
   
     | id | name      |
     |----|-----------|
     | 1  |   John    |
     | 2  |   Jane    |
   
     ```sql
     SELECT TRIM(name) AS trimmed_name FROM table_name;
     ```
   
     结果表：
   
     | trimmed_name |
     |--------------|
     | John         |
     | Jane         |

2. 日期和时间函数：

   - NOW函数：用于返回当前日期和时间。
   
     ```sql
     SELECT NOW() AS current_datetime;
     ```
   
     结果表：
   
     | current_datetime       |
     |------------------------|
     | 2022-01-01 12:34:56    |
   
   - DATE_FORMAT函数：用于将日期格式化为指定的字符串。
   
     示例表：
   
     | id | birth_date          |
     |----|---------------------|
     | 1  | 1990-05-15          |
     | 2  | 1985-10-20          |
   
     ```sql
     SELECT DATE_FORMAT(birth_date, '%Y-%m-%d') AS formatted_date FROM table_name;
     ```
   
     结果表：
   
     | formatted_date |
     |----------------|
     | 1990-05-15     |
     | 1985-10-20     |

3. 聚合函数：

   - COUNT函数：用于计算指定列中的行数。
   
     示例表：
   
     | id | name    |
     |----|---------|
     | 1  | John    |
     | 2  | Jane    |
   
     ```sql
     SELECT COUNT(*) AS total_count FROM table_name;
     ```
   
     结果表：
   
     | total_count |
     |-------------|
     | 2           |

     此外COUNT还可以与DISCINCT
   
   - SUM函数：用于计算指定列的总和。
   
     示例表：
   
     | id | price |
     |----|-------|
     | 1  | 100   |
     | 2  | 200   |
   
     ```sql
     SELECT SUM(price) AS total_price FROM table_name;
     ```
   
     结果表：
   
     | total_price |
     |-------------|
     | 300         |



    - MAX函数：用于计算指定列的总和。
   
        示例表：
    
        | id | price |
        |----|-------|
        | 1  | 100   |
        | 2  | 200   |
    
        ```sql
        SELECT MAX(price) AS max_price FROM table_name;
        ```
    
        结果表：
    
        | max_price |
        |-----------|
        | 200       |



   - MIN函数：用于计算指定列的总和。
   
     示例表：
   
     | id | price |
     |----|-------|
     | 1  | 100   |
     | 2  | 200   |
   
     ```sql
     SELECT MIN(price) AS min_price FROM table_name;
     ```
   
     结果表：
   
     | min_price |
     |-------------|
     | 100         | 



这些只是MySQL中的一些常见函数示例，还有许多其他函数可用于处理和操作数据。你可以在MySQL官方文档中找到更多详细的函数列表和示例。