### 17. GROUP BY 关键字
GROUP BY关键字是在SQL中用于对查询结果进行分组的关键字。它将查询结果按照指定的列或表达式进行分组，并对每个分组应用聚合函数（如SUM、COUNT、AVG等）。

语法：
```sql
SELECT 列名, 聚合函数
FROM 表名
GROUP BY 列名;
```

示例：
```sql
SELECT department, COUNT(*) as count
FROM employees
GROUP BY department;
```

示例说明：
以上示例将从"employees"表中选择"department"列，并对其进行分组。然后，对每个部门应用COUNT(*)聚合函数，计算每个部门的员工数量。结果将按照部门分组返回。

GROUP BY关键字常与聚合函数一起使用，以便对每个分组进行计算和汇总。它可以用于SELECT语句中，也可以与HAVING子句一起使用，以进一步筛选分组结果。注意，GROUP BY子句中的列名必须与SELECT子句中的列名一致，或者是聚合函数的参数。GROUP BY是一种用于对结果集进行分组的SQL子句。它通常与聚合函数一起使用，以便对每个组应用聚合函数并返回汇总结果。下面是一个示例表和相应的代码来说明GROUP BY的用法：

示例表：orders

| order_id | customer_id | order_date | total_amount |
|----------|-------------|------------|--------------|
| 1        | 1001        | 2022-01-01 | 100          |
| 2        | 1002        | 2022-01-02 | 200          |
| 3        | 1001        | 2022-01-03 | 150          |
| 4        | 1003        | 2022-01-04 | 300          |
| 5        | 1002        | 2022-01-05 | 250          |

代码示例：

```sql
SELECT customer_id, SUM(total_amount) AS total_spent
FROM orders
GROUP BY customer_id;
```

结果：

| customer_id | total_spent |
|-------------|-------------|
| 1001        | 250         |
| 1002        | 450         |
| 1003        | 300         |

在上面的示例中，我们使用GROUP BY子句按customer_id对订单进行分组。然后，我们使用SUM函数计算每个客户的总消费金额，并将其命名为total_spent。最后，我们得到了每个客户的customer_id和对应的总消费金额。

请注意，GROUP BY子句必须与SELECT语句中的列名一起使用，这些列名要么是分组的列，要么是聚合函数的参数。在示例中，customer_id是分组的列，而SUM(total_amount)是聚合函数的参数。

使用GROUP BY可以对结果集进行更细粒度的分组和聚合操作，以便获得更有意义的汇总数据。
