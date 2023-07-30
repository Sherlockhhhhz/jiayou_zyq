### 03 SQL JOINS 
在SQL语言中，JOIN关键字用于将两个或多个表中的数据连接在一起，以便进行更复杂的查询和分析。JOIN操作是SQL中非常重要和常用的功能，它允许我们在多个表之间建立关联，从而获取更全面和有用的数据。

在SQL中，JOIN是用于将两个或多个表中的行组合在一起的操作。它基于表之间的关联关系，将相关的行连接起来，以便进行更复杂的查询和分析。
<img src="../image/sql-join.png">
常见的JOIN类型包括：

### 1. INNER JOIN:
返回两个表中匹配的行。只有在连接条件满足时，才会返回结果。

`INNER JOIN` 关键字语法
```sql
SELECT column_name(s)
FROM table_name1
INNER JOIN table_name2
ON table_name1.column_name=table_name2.column_name
```
实例表:

**Persons表**
|Id_P	|LastName	|FirstName	|Address	|City
|---|-------|-------|-------|-------|
|1	|Adams	|John	|Oxford Street	|London
|2	|Bush	|George	|Fifth |Avenue	|New York
|3	|Carter	|Thomas	|Changan |Street	|Beijing


**Orders表**
|Id_O	|OrderNo	|Id_P
|----|-----|----|
|1	|77895	|3
|2	|44678	|3
|3	|22456	|1
|4	|24562	|1
|5	|34764	|65

```sql
SELECT Persons.LastName, Persons.FirstName, Orders.OrderNo
FROM Persons
INNER JOIN Orders
ON Persons.Id_P=Orders.Id_P
ORDER BY Persons.LastName
```

**结果表:**
|LastName	|FirstName	|OrderNo
|------|-------|------|
|Adams	|John	|22456
|Adams	|John	|24562
|Carter	|Thomas	|77895
|Carter	|Thomas	|44678

INNER JOIN 关键字在表中存在至少一个匹配时返回行。如果 "Persons" 中的行在 "Orders" 中没有匹配，就不会列出这些行。

### 2. LEFT JOIN（或LEFT OUTER JOIN）：
返回左表中的所有行，以及右表中与左表匹配的行。如果右表中没有匹配的行，则返回NULL值。

`LEFT JOIN` 关键字语法
```sql
SELECT column_name(s)
FROM table_name1
LEFT JOIN table_name2
ON table_name1.column_name=table_name2.column_name
```
实例表:

**Persons表**
|Id_P	|LastName	|FirstName	|Address	|City
|---|-------|-------|-------|-------|
|1	|Adams	|John	|Oxford Street	|London
|2	|Bush	|George	|Fifth |Avenue	|New York
|3	|Carter	|Thomas	|Changan |Street	|Beijing


**Orders表**
|Id_O	|OrderNo	|Id_P
|----|-----|----|
|1	|77895	|3
|2	|44678	|3
|3	|22456	|1
|4	|24562	|1
|5	|34764	|65

```sql
SELECT Persons.LastName, Persons.FirstName, Orders.OrderNo
FROM Persons
LEFT JOIN Orders
ON Persons.Id_P=Orders.Id_P
ORDER BY Persons.LastName
```

**结果表:**
|LastName	|FirstName	|OrderNo
|-------|-------|------|
|Adams	|John	|22456
|Adams	|John	|24562
|Carter	|Thomas	|77895
|Carter	|Thomas	|44678
|Bush	|George	 |NULL

### 3. RIGHT JOIN（或RIGHT OUTER JOIN）：
返回右表中的所有行，以及左表中与右表匹配的行。如果左表中没有匹配的行，则返回NULL值。

`RIGHT JOIN` 关键字语法
```sql
SELECT column_name(s)
FROM table_name1
RIGHT JOIN table_name2
ON table_name1.column_name=table_name2.column_name
```
实例表:

**Persons表**
|Id_P	|LastName	|FirstName	|Address	|City
|---|-------|-------|-------|-------|
|1	|Adams	|John	|Oxford Street	|London
|2	|Bush	|George	|Fifth |Avenue	|New York
|3	|Carter	|Thomas	|Changan |Street	|Beijing


**Orders表**
|Id_O	|OrderNo	|Id_P
|----|-----|----|
|1	|77895	|3
|2	|44678	|3
|3	|22456	|1
|4	|24562	|1
|5	|34764	|65

```sql
SELECT Persons.LastName, Persons.FirstName, Orders.OrderNo
FROM Persons
RIGHT JOIN Orders
ON Persons.Id_P=Orders.Id_P
ORDER BY Persons.LastName
```
**结果表:**
|LastName|	FirstName	|OrderNo
|------|------|------|
|Adams	|John	|22456
|Adams	|John	|24562
|Carter	|Thomas	|77895
|Carter	|Thomas	|44678
| NULL |NULL	 	|34764

RIGHT JOIN 关键字会从右表 (Orders) 那里返回所有的行，即使在左表 (Persons) 中没有匹配的行。



### 4. FULL JOIN（或FULL OUTER JOIN）：
返回左表和右表中的所有行，如果没有匹配的行，则返回NULL值。
`FULL JOIN`关键字语法
```sql
SELECT column_name(s)
FROM table_name1
FULL JOIN table_name2
ON table_name1.column_name=table_name2.column_name
```
实例表:

**Persons表**
|Id_P	|LastName	|FirstName	|Address	|City
|---|-------|-------|-------|-------|
|1	|Adams	|John	|Oxford Street	|London
|2	|Bush	|George	|Fifth |Avenue	|New York
|3	|Carter	|Thomas	|Changan |Street	|Beijing


**Orders表**
|Id_O	|OrderNo	|Id_P
|----|-----|----|
|1	|77895	|3
|2	|44678	|3
|3	|22456	|1
|4	|24562	|1
|5	|34764	|65

```sql
SELECT Persons.LastName, Persons.FirstName, Orders.OrderNo
FROM Persons
FULL JOIN Orders
ON Persons.Id_P=Orders.Id_P
ORDER BY Persons.LastName
```
|LastName	|FirstName	|OrderNo
|------|-------|-----|
|Adams	|John	|22456
|Adams	|John	|24562
|Carter	|Thomas	|77895
|Carter|	Thomas	|44678
|Bush|	George	 |NULL
|NULL| 	NULL 	|34764|

FULL JOIN 关键字会从左表 (Persons) 和右表 (Orders) 那里返回所有的行。如果 "Persons" 中的行在表 "Orders" 中没有匹配，或者如果 "Orders" 中的行在表 "Persons" 中没有匹配，这些行同样会列出。


### 总结
JOIN操作通常需要指定连接条件，这是通过使用ON子句或WHERE子句来实现的。连接条件定义了连接两个表的列之间的关系。
