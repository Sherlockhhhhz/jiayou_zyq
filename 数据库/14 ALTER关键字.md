### 14. ALTER 关键字
ALTER关键字是MySQL中用于修改数据库表结构的关键字。它可以用于添加、修改或删除表的列、约束、索引等。

下面是一些ALTER关键字的示例：

1. 添加列：
   ```sql
   ALTER TABLE 表名
   ADD 列名 数据类型;
   ```

   示例：
   ```sql
   ALTER TABLE students
   ADD age INT;
   ```

2. 修改列：
   ```sql
   ALTER TABLE 表名
   MODIFY 列名 新数据类型;
   ```

   示例：
   ```sql
   ALTER TABLE students
   MODIFY age VARCHAR(50);
   ```

3. 删除列：
   ```sql
   ALTER TABLE 表名
   DROP COLUMN 列名;
   ```

   示例：
   ```sql
   ALTER TABLE students
   DROP COLUMN age;
   ```

4. 添加主键：
   ```sql
   ALTER TABLE 表名
   ADD PRIMARY KEY (列名);
   ```

   示例：
   ```sql
   ALTER TABLE students
   ADD PRIMARY KEY (id);
   ```

5. 添加外键：
   ```sql
   ALTER TABLE 表名
   ADD FOREIGN KEY (列名) REFERENCES 参考表名(参考列名);
   ```

   示例：
   ```sql
   ALTER TABLE orders
   ADD FOREIGN KEY (customer_id) REFERENCES customers(id);
   ```

这些示例只是ALTER关键字的一小部分用法，MySQL的ALTER语句还有很多其他功能，如修改表名、修改表的存储引擎等。具体使用时，可以根据需要选择适当的ALTER语句来修改数据库表结构。