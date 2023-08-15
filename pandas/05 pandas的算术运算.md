### 05 pandas的算术运算
1. [数据对齐](#1)
2. [填充缺失值fill_value](#2)
<h4 id="1"> 1. 数据对齐</h4>
pandas最重要的一个功能是，它可以对不同索引的对象进行算术运算。<u>在将对象相加时，如果存在不同的索引对，则结果的索引就是该索引对的并集。</u>对于有数据库经验的用户，这就像在索引标签上进行自动外连接。看一个简单的例子：
```python
import pandas as pd
s1 = pd.Series([7.3, -2.5, 3.4, 1.5], index=['a', 'c', 'd', 'e'])
s2 = pd.Series([-2.1, 3.6, -1.5, 4, 3.1], index=['a', 'c', 'e', 'f', 'g'])
print(s1)
Output: 
a   7.3
c   -2.5
d   3.4
e   1.5
dtype: float64

print(s2)
Output: 
a   -2.1
c   3.6
e   -1.5
f   4.0
g   3.1
dtype: float64
```
将它们相加就会产生:
```python
print(s1 + s2)
Output: 
a   5.2
c   1.1
d   NaN
e   0.0
f   NaN
g   NaN
dtype: float64
```
自动的数据对齐操作在不重叠的索引处引入了`NA`值。缺失值会在算术运算过程中传播。
对于DataFrame，<u>对齐操作会同时发生在行和列上</u>：
```python
df1 = pd.DataFrame(np.arange(9.).reshape((3, 3)), columns=list('bcd'),
index=['Ohio', 'Texas', 'Colorado'])
df2 = pd.DataFrame(np.arange(12.).reshape((4, 3)), columns = list('bde'), index = ["Utah", "Ohio", "Texas", "Oregon"])
print(df1)
Output:
         b    c    d
Ohio     0.0  1.0  2.0
Texas    3.0  4.0  5.0
Colorado 6.0  7.0  8.0

print(df2)
Output:
       b    d    e
Utah   0.0  1.0  2.0
Ohio   3.0  4.0  5.0
Texas  6.0  7.0  8.0
Oregon 9.0  10.0 11.0
```
把它们相加后将会返回一个新的DataFrame，其索引和列为原来那两个DataFrame的并集：
```python
print(df1 + df2)
Output:
         b    c    d    e
Colorado NaN  NaN  NaN  NaN
Ohio     3.0  NaN  6.0  NaN
Oregon   NaN  NaN  NaN  NaN
Texas    9.0  NaN  12.0 NaN
Utah     NaN  NaN  NaN  NaN
```
因为'c'和'e'列均不在两个DataFrame对象中，在结果中以缺省值呈现。行也是同样。
如果DataFrame对象相加，没有共用的列或行标签，结果都会是空：
```python
df1 = pd.DataFrame({'A': [1, 2]})
df2 = pd.DataFrame({'B': [3, 4]})
print(df1)
Output:
    A
0   1
1   2

print(df2)
Output:
    B
0   3
1   4

print(df1 - df2)
Output:
   A    B
0  NaN  NaN
1  NaN  NaN
```
<h4 id = "2">2. 填充值fill_value</h4>
在对不同索引的对象进行算术运算时，你可能希望当一个对象中某个轴标签在另一个对象中找不到时填充一个特殊值（比如0）：
```python
df1 = pd.DataFrame(np.arange(12.).reshape((3, 4)), columns=list('abcd'))
df2 = pd.DataFrame(np.arange(20.).reshape((4, 5)), columns=list('abcde'))

df2.loc[1, 'b'] = np.nan # 使第一行'b'索引对应的值修改为NAN缺失值
print(df1)
Output:
    a   b   c    d
0 0.0 1.0 2.0  3.0
1 4.0 5.0 6.0  7.0
2 8.0 9.0 10.0 11.0

print(df2)
Output:
   a    b    c    d    e
0  0.0  1.0  2.0  3.0  4.0
1  5.0  NaN  7.0  8.0  9.0
2  10.0 11.0 12.0 13.0 14.0
3  15.0 16.0 17.0 18.0 19.0
```
将它们相加时，没有重叠的位置就会产生NA值：
```python
print(df1 + df2)
Output:
   a    b    c    d    e
0  0.0  2.0  4.0  6.0  NaN
1  9.0  NaN  13.0 15.0 NaN
2  18.0 20.0 22.0 24.0 NaN
3  NaN  NaN  NaN  NaN  NaN
```
使用df1的add方法，传入df2以及一个`fill_value`参数：
```python
print(df1.add(df2, fill_value = 0)) # 把缺失值看做成0, 如果想把缺失值看成其他值就改成其他值就OK
Output:
   a    b    c    d    e
0  0.0  2.0  4.0  6.0  4.0
1  9.0  5.0  13.0 15.0 9.0
2  18.0 20.0 22.0 24.0 14.0
3  15.0 16.0 17.0 18.0 19.0
```
下表列出了Series和DataFrame的算术方法。它们每个都有一个副本，以字母r开头，它会翻转参数。因此这两个语句是等价的：
```python
print(1 / df1)
Output: 
   a        b        c        d
0  inf      1.000000 0.500000 0.333333
1  0.250000 0.200000 0.166667 0.142857
2  0.125000 0.111111 0.100000 0.090909

# 1 / df1 与 df1.rdiv(1)等价
print(df1.rdiv(1))
Output: 
   a        b        c        d
0  inf      1.000000 0.500000 0.333333
1  0.250000 0.200000 0.166667 0.142857
2  0.125000 0.111111 0.100000 0.090909
```

这些方法跟运算符都是一一对应的关系, 一般了解运算符就OK了, 但是比如一些源码上面出现mul这些函数, 你要知道这些函数的作用是什么, 但是需要记住用函数的好处, 可以指定参数来完成更多的功能
|方法|说明|
|----|----|
|add, radd|用于加法(+)的方法|
|sub, rsub|用于减法(-)的方法|
|div, rdiv|用于除法(/)的方法|
|floordiv, rfloordiv|用于整数(//)的方法|
|mul, rmul|用于乘法(*)的方法|
|pow, rpow|用于指数(**)的方法|

<h4 id="3"> 3. DataFrame和Series之间的运算</h4>

跟不同维度的NumPy数组一样，`DataFrame`和`Series`之间算术运算也是有明确规定的。先来看一个具有启发性的例子，计算一个二维数组与其某行之间的差：
```python
arr = np.arange(12.).reshape((3, 4))
print(arr)
Output:
array([ [ 0., 1., 2., 3.],
        [ 4., 5., 6., 7.],
        [ 8., 9., 10., 11.] ])

print(arr[0])
Output: 
array([ 0., 1., 2., 3.])

print(arr - arr[0]) # 广播性质, numpy会把arr[0]变成和arr一样的形状(4 * 4)
array([ [ 0., 0., 0., 0.],
        [ 4., 4., 4., 4.],
        [ 8., 8., 8., 8.] ])

```
当我们从arr减去arr[0]，每一行都会执行这个操作。这就叫做广播(broadcasting)：
```python
frame = pd.DataFrame(np.arange(12.).reshape((4, 3)), columns=list('bde'),
index=['Utah', 'Ohio', 'Texas', 'Oregon'])
series = frame.iloc[0]
print(frame)
Output:
       b   d    e
Utah   0.0 1.0  2.0
Ohio   3.0 4.0  5.0
Texas  6.0 7.0  8.0
Oregon 9.0 10.0 11.0

print(series)
Output: 
b   0.0
d   1.0
e   2.0
Name: Utah, dtype: float64
```
默认情况下，DataFrame和Series之间的算术运算会将Series的索引匹配到DataFrame的列，然后沿着行一直向下<u>广播</u>：
```python
print(frame - series)
Output: 
       b   d   e
Utah   0.0 0.0 0.0
Ohio   3.0 3.0 3.0
Texas  6.0 6.0 6.0
Oregon 9.0 9.0 9.0
```
如果某个索引值在DataFrame的列或Series的索引中找不到，则参与运算的两个对象就会被重新索引以形成并集：
```python
series2 = pd.Series(range(3), index=['b', 'e', 'f'])
print(frame + series2)
Output: 
       b    d    e    f
Utah   0.0  NaN  3.0  NaN
Ohio   3.0  NaN  6.0  NaN
Texas  6.0  NaN  9.0  NaN
Oregon 9.0  NaN  12.0 NaN
```
如果你希望匹配行且在列上广播，则必须使用算术运算方法。例如：
```python
series3 = frame['d']
print(frame)
Output: 
       b   d    e
Utah   0.0 1.0  2.0
Ohio   3.0 4.0  5.0
Texas  6.0 7.0  8.0
Oregon 9.0 10.0 11.0

print(series3)
Output: 
Utah   1.0
Ohio   4.0
Texas  7.0
Oregon 10.0
Name: d, dtype: float64

print(frame.sub(series3, axis='index'))
Output:
        b    d    e
Utah   -1.0 0.0 1.0
Ohio   -1.0 0.0 1.0
Texas  -1.0 0.0 1.0
Oregon -1.0 0.0 1.0
```
传入的轴号就是希望匹配的轴。在本例中，我们的目的是匹配DataFrame的行索引（<u>axis='index'or axis=0</u>）并进行广播。
