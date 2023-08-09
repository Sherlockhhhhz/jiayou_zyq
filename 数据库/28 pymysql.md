### 28. pymysql
要想在python中使用数据库，我们需要第三方库，常用的是pymysql模块，下面我们来认识一下。

#### 1. pymysql的使用
核心五步:
1. 连接数据库
2. 创建游标对象
3. 对数据库进行增删改查
4. 关闭游标
5. 关闭游标


首先，必须先和数据库建立一个传输数据的连接通道，需要用到pymysql下的`connect()`方法, `pymysql.connect()` 方法返回的是Connections模块下的Connection 实例，`connect()` 方法传参就是在给`Connection`类的 _init_ 初始化魔术方法参数，也可以理解为 connect() 方法就是在创建新的 `Connetion` 类。

下表是connect()的参数
|参数      |说明|
|---------------|----|
|host      |主机ip|
|user      |用户名|
|password  |密码|
|database  |数据库|
|port      |端口号|
|charset   |字符集|

```python
db = pymysql.connect(host='localhost', 
　　　　　　　　　　　　　　user='root',
　　　　　　　　　　　　　　password='123456', 
　　　　　　　　　　　　　　database='db1',   # 所用的数据库名
　　　　　　　　　　　　　　charset = 'utf-8')
```
在使用pymysql.connect() 方法与数据库建立连接后，想要操作数据库时，就需要使用游标 `Cursor`通过连接好的数据库（此处为db）调用 `cursor()` 方法即可返回一个新的游标对象，在连接没有关闭之前，游标对象可以反复使用。
```python
cursor = db.cursor()
```
数据库操作需要使用`Cursor`类的实例（即通过 `db.cursor()` 创建的 cursor 游标对象）提供的 `execute()` 方法，执行SQL语句，成功则返回结果
​例如：插入操作:
```python
sql = "insert into user_pwd(username,password) values('vera', '1234')" 
cursor.execute(sql)
```
这里插入数据的时候插入的表名有个需要注意的地方，插入表名的时候最好带着库名，例如:
```python
sql = "insert into db1.table(username, password)  values('xxx', '123')"
```
否则可能会容易报错

**查询操作**
```python
sql = "select * from table"
response1 = cursor.execute(sql)
response2 = cursor.fetchall()
```
这里有两个response返回，`response1`是对cursor.execute(sql) 的返回数据接收，这个返回可能并不是你想要的返回值，因为它返回的是**查询到的个数**，是个`int`类型的数字

而我想response2才是你想要的返回response2是调用了`fetchall`方法：查询时获取结果集中的所有行，**一行构成一个元组，然后再将这些元组返回（即嵌套元组）**
还有一些别的方法如下
|名称|说明|
|----|----|
|fetchone()|获取结果集的下一行|
|fetchmany(size=None)	|size指定返回的行数,None则返回空元组|
|fetchall()|返回剩下的所有行,如果走到末尾,就返回空元组,否则返回一个元组,其元素是每一行的记录封装的一个元组|
|cursor.rownumber|返回当前行号.可以修改,支持负数|
|cursor.rowcount|返回的总行数|
**注意:**fetch操作的是结果集，结果集是保存在客户端的，也就是说fetch的时候，查询已经结束了

#### 2. 事务
`Connection`类提供了三个方法： `begin`开始事务，`commit`提交事务， `rollback`回滚事务，如果通过sql语句对数据库中的数据进行了修改，则需要提交事务。
rollback()也是个很重要的方法，正确的使用rollback可以避免commit提交事务的时候发生错误导致程序中断。主要使用方式：结合try except捕获异常，将事务进行rollback回滚

```python
数据库代码
try:	
 	db.commit()
except Exception as e:
 	db.rollback()
cursor.close() # 先关闭游标
db.close() # 再关闭数据库连接
```
释放资源，在程序结束时需要建立的连接即建立的游标资源释放掉，避免资源的浪费，可以调用close() 方法
