### 25. UNION关键字
UNION根据我们在SELECT中指定的列，把两张或者多张表的查询结果合并到一张表中，可以把UNION的查询结果相成"重叠了"


Websites表:
```sql
mysql> SELECT * FROM Websites;
+----+--------------+---------------------------+-------+---------+
| id | name         | url                       | alexa | country |
+----+--------------+---------------------------+-------+---------+
| 1  | Google       | https://www.google.cm/    | 1     | USA     |
| 2  | 淘宝          | https://www.taobao.com/   | 13    | CN      |
| 3  | 菜鸟教程      | http://www.runoob.com/    | 4689  | CN      |
| 4  | 微博          | http://weibo.com/         | 20    | CN      |
| 5  | Facebook     | https://www.facebook.com/ | 3     | USA     |
| 7  | stackoverflow | http://stackoverflow.com/ |   0 | IND     |
+----+---------------+---------------------------+-------+---------+
```
APP表:
```sql
mysql> SELECT * FROM apps;
+----+------------+-------------------------+---------+
| id | app_name   | url                     | country |
+----+------------+-------------------------+---------+
|  1 | QQ APP     | http://im.qq.com/       | CN      |
|  2 | 微博 APP | http://weibo.com/       | CN      |
|  3 | 淘宝 APP | https://www.taobao.com/ | CN      |
+----+------------+-------------------------+---------+
```
```sql
SELECT country FROM Websites
UNION
SELECT country FROM apps
ORDER BY country;
```
查询结果
|country|
|-------|
|CN|
|IND|
|USA|

**UNION关键字的限制**

1. 每个SELECT语句中列的数量必须一致 , 不可以由第一条语句选取了两列, 其他语句却选取一列。

2. 每个SELECT语句包含的表达式与统计函数也必须相同。

3. SELECT语句的顺序不重要， 不会改变结果。

4. SQL默认会清除联合结果中的重复值。

5. 列的数据类型必须相同或者可以互相转换。

6. 如果处于某些原因而需要看到重复数据，可以使用`UNION ALL`关键字。这个关键字可以返回每个相符的记录， 而不只是没有重复的记录。

7. CREATE TABLE 表名 AS 可以捕获UNION的结果，以新建出新的表。
