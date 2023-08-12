### 29 MySQL用户与账号
#### 1. 根用户root
默认情况下, 第一位用户——**根**用户具有所有数据库操控能力。这一点很重要, 因为根用户必须可以为其他用户创建账号。我们并不想限制根用户的权限, 但他的账号应该有密码。MySQL设定根用户密码的方法很简单:
```sql
// 根用户的名称是root
// localhost代表安装与运行SQL软件的机器, 也就是你正在使用的这台计算机
SET PASSWORD FOR 'root@localhost' = PASSWORD('123456');
```
<u>如何设定密码并非重点, 重点在于一定要设置密码</u>

#### 2. 添加新用户以及赋予权限GRANT
```sql
// elsie为增设的用户名称
CREATE USER elsie INDENTIFIED BY '123456789';

// 可以给用户赋予权限, 使它可以操作数据库中的一些表以及执行某些权限
// 通过GRANT关键字可以完成上述操作
// 下面代码的作用是给用户elsie对于指定表有SELECT的权限
GRANT SELECT ON 表名 TO elsie;

// 如果需要给elsie用户在user表中使用INSERT的权限怎么办呢
GRANT INSERT ON user TO elsie;
```

#### 3. REVOKE
假设要把赋予给elsie用户的SELECT权限收回, 此时需要使用`REVOKE`语句。

还记得最简单的`GRANT`语句吗 ? `REVOKE`语句的语法几乎与它完全相同, 只是把GRANT换成REVOKE， TO换成FROM而已。
```sql
REVOKE SELECT ON 表名 FROM elsie;
```

