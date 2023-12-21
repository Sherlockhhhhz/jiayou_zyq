```python 
main.py文件
class Ocr_demo():
    def __init__(self):
        self.login_window = Login_window()  # 登录界面窗口
        self.main_window = MainWindow()  # 主界面窗口
        self.worker = worker()  # 用户
        self.index = 0  # 索引
        try:
            self.db = pymysql.connect(  # 连接数据库, 这里作为属性的原因是, 有很多函数都需要连接数据库, 直接作为属性, 可以减小程序开销
                host='localhost',
                user="root",
                password='123456789',
                database='db1'
            )
        except:
            self.db = None # 数据库连接失


        self.connect()  # 运行控件连接函数
```
1. self.login_window -> 登录界面窗口, 里面是有self.show()函数, 也就是说只要实例化Login_window这个类，这个窗口就会展现出来。🏜️

```python
login_window.py文件
class  Login_window(QWidget):
    def __init__(self):
        super(Login_window, self).__init__()
        self.setupUi()
        self.show()
        self.connect()
```

2. self.main_window -> 主界面窗口, 里面没有self.show(), 要想展现这个界面，需要我们手动在main.py中调用self.main_window.show()。🗻

3. self.worker -> 表示我们每个员工对应的类, 因为没有定好数据库, 这里用不到了。🏛️

4. self.index 主要用于我们在文件夹显示窗口中, 向上或向下选取图片。🗽

<img src="../image/index.bmp"></img>

5. self.db我们的数据库, 其中的参数🗼
```sql
1. host='localhost'对应我们自己的电脑, 如果想要用我们的电脑连接其他电脑的数据库, 这里要改成其他电脑的ip地址
2. user='root', 表示我们用root用户来操作数据库, root用户表示最高权限。
3. password 表示我们数据库的密码
4. database表示我们所使用的的数据库名称, 这里是db1数据库
``````
这里的try-except语句的作用是，因为这个代码会在不同的电脑上运行，不是所有电脑的数据库跟这上面所显示的信息一样，⛩️所以如果不一样，就会发生报错，我们用try语句来防止报错是程序直接退出，🕍如果所运行的电脑没有数据库，我们就将数据库设为None,表示空。🛕
