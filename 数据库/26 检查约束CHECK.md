### 26. 检查约束CHECK
在前面我们已经开过几种关于列的约束。约束限定了可以插入列的内容，而在我们创建表时就要加入约束。`NOT NULL`, `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`都是常见的约束。

还有一种约束称为CHECK，下面为其范例。假设我们有一个小猪存钱罐，我们想追踪放入存钱罐的硬币数量，硬币面额可能是P, N, D, Q,均以首字母缩写表示。创建小猪存钱罐时， 即可用`CHECK`约束来限制插入coin列的值。
```
CHECK约束限定允许插入某个列的值。它与WHERE子句都使用相同的条件表达式。
```
```sql
CREATE TABLE piggy_bank(
    id INT NOT NULL PRIMARY KEY,
    coin CHAR(1) CHECK (coin IN ('P', 'N', 'D, 'Q'))
)
```
如果插入的值无法通过CHECK条件，则出现错误信息。