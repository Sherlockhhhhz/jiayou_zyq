### 07. time模块
`Python` 语言能用很多方式处理日期和时间，转换日期格式是一个常见的功能。

`Python`提供了一个`time`模块可以用于格式化日期和时间。

时间间隔是以秒为单位的浮点小数。

每个时间戳都以自从1970年1月1日午夜（历元）经过了多长时间来表示。

`Python` 的 `time` 模块下有很多函数可以转换常见日期格式。如函数`time.time()`用于获取当前时间戳, 如下实例:
```python
import time

ticks = time.time()
print(f"当前时间戳为: {ticks}")
```
以上实例输出结果：
```python
当前时间戳为: 1459994552.51
```
时间戳单位最适于做日期运算。但是`1970`年之前的日期就无法以此表示了。太遥远的日期也不行，`UNIX`和`Windows`只支持到`2038`年。

要将时间戳转换为易读的格式，你可以使用time库中的time.localtime()函数和time.strftime()函数。

下面是一个示例代码，演示了如何将时间戳转换为易读的格式：

```python
import time

timestamp = 1629876543  # 假设这是一个时间戳

# 将时间戳转换为本地时间的时间元组
time_tuple = time.localtime(timestamp)

# 将时间元组格式化为易读的字符串
readable_time = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)

print(readable_time)
```

在上面的示例中，我们首先使用time.localtime()函数将时间戳转换为本地时间的时间元组。然后，我们使用time.strftime()函数将时间元组格式化为指定的易读格式。在这个例子中，我们使用"%Y-%m-%d %H:%M:%S"作为格式字符串，它表示年-月-日 时:分:秒的格式。

你可以根据自己的需求选择不同的格式字符串，以获得你想要的易读时间格式。

除了time.time()此外，另外一个常用的函数为time.sleep(seconds):暂停程序执行指定的秒数。
```python
import time
time.sleep(1) # 意为暂停1s
```