### 9. LIKE  和 通配符
通配符是在模式匹配中使用的特殊字符，而"LIKE"关键字用于在MySQL中进行模式匹配查询。下面是通配符和"LIKE"关键字的介绍以及代码示例：

1. 百分号（%）通配符：表示任意字符出现任意次数（包括零次）。例子：
 ```sql
 SELECT * FROM students WHERE name LIKE 'J%';
 ```
<span style="color:pink;">上述代码将返回名字以字母"J"开头的学生记录。</span>

2. 下划线（_）通配符：表示匹配任意单个字符。例子：
 ```sql
 SELECT * FROM students WHERE name LIKE 'J_n';
 ```
<span style="color:pink">上述代码将返回名字以字母"J"开头，后面是任意一个字符，然后是字母"n"的学生记录。</span>

3. 方括号（[]）通配符：用于指定一个字符集合中的任意一个字符。例子：
 ```sql
 SELECT * FROM students WHERE name LIKE '[JM]ohn';
```
<span style="color:pink">上述代码将返回名字以字母"J"或"M"开头，然后是字母"ohn"的学生记录。</span>

4. 反向方括号（[^]）通配符：用于指定一个字符集合中除了指定字符之外的任意一个字符。例子：
```sql
SELECT * FROM students WHERE name LIKE '[^A-Z]%';
```
<span style="color:pink;">上述代码将返回名字不以大写字母开头学生记录。</span>

"LIKE"关键字与通配符结合使用，可以进行模式匹配查询。它可以在SELECT语句的WHERE子句中使用，用于筛选满足特定模式的数据。
请注意，在使用通配符和"LIKE"关键字时，要注意模式的书写和匹配规则，以确保查询条件的正确性和预期结果。
以下是一个综合示例：
 ```sql
SELECT * FROM students WHERE name LIKE 'J%hn' OR name LIKE 'M%';
 ```
上述代码将返回名字以字母"J"开头，后面是任意字符，然后是字母"hn"的学生记录，以及名字以字母"M"开头的学生记录。