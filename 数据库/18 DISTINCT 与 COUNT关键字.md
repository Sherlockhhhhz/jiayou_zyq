

### 19. DISTINCT 关键字 与 COUNT 关键字
当结合使用DISTINCT和COUNT时，可以统计某一列中不重复值的数量。下面是一个示例表和相应的代码：

假设有一个名为"orders"的表，包含以下列：order_id、customer_id和product_name。我们想要统计不同产品的数量。

表格示例：

| order_id | customer_id | product_name |
|----------|-------------|--------------|
| 1        | 100         | A            |
| 2        | 100         | B            |
| 3        | 200         | A            |
| 4        | 300         | C            |
| 5        | 300         | C            |
| 6        | 400         | B            |

代码示例：

```sql
SELECT COUNT(DISTINCT product_name) AS distinct_count
FROM orders;
```

运行以上代码后，将返回一个名为"distinct_count"的列，其中包含不同产品的数量。在上述示例中，结果将是3，因为有3种不同的产品（A、B和C）。

使用DISTINCT和COUNT的组合可以帮助我们统计某一列中不重复值的数量，从而得到更详细的统计信息。