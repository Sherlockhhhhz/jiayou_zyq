### 04 pandas的基本功能
我将介绍操作Series和DataFrame中的数据的基本手段。后续将更加深入地挖掘
pandas在数据分析和处理方面的功能。

1. [重新索引reindex](#1)
2. [删除指定数据drop](#2)
3. [索引与切片](#3)
4. [用loc与iloc进行索引](#4)

<h3 id="1">1. 重新索引reindex</h2>
pandas对象的一个重要方法是reindex，其作用是创建一个<u>新对象</u>，它的数据符合新的索引。看下面的例子：

```python
obj = pd.Series([4.5, 7.2, -5.3, 3.6], index=['d', 'b', 'a', 'c'])
print(obj)
Output: 
d   4.5
b   7.2
a   -5.3
c   3.6
dtype: float64
```
用该Series的`reindex`将会根据新索引进行重排。<u>如果某个索引值当前不存在，就引入缺失值</u>：
```python
obj2 = obj.reindex(['a', 'b', 'c', 'd', 'e'])
print(obj2)
Ouptut: 
a  -5.3
b  7.2
c  3.6
d  4.5
e  NaN # 注意因为obj不存在e索引, 所以此处为NAN缺失值
dtype: float64
```
对于时间序列这样的有序数据，重新索引时可能需要做一些插值处理。`method`选项即可达到此目的，例如，使用`ffill`可以实现前向值填充(向前填充的意思是如果i索引不存在, 则它的值为i-1索引对应的值)：
```python
obj3 = pd.Series(['blue', 'purple', 'yellow'], index=[0, 2, 4])
obj4 = obj3.reindex(range(6), method='ffill')
print(obj4)
Output: 
0   blue
1   blue
2   purple
3   purple
4   yellow
5   yellow
dtype: object
```
借助DataFrame，reindex可以修改（行）索引和列。只传递一个序列时，会重新索引结果的行：
```python
frame = pd.DataFrame(np.arange(9).reshape((3, 3)),
index=['a', 'c', 'd'],
columns=['Ohio', 'Texas', 'California'])
print(frame)
Output: 
    Ohio Texas California
a   0    1     2
c   3    4     5
d   6    7     8

frame2 = frame.reindex(['a', 'b', 'c', 'd'])
print(frame2)
Output: 
   Ohio Texas California
a  0.0  1.0   2.0
b  NaN  NaN   NaN
c  3.0  4.0   5.0
d  6.0  7.0   8.0
```
列可以用`columns`关键字重新索引：
```python
states = ['Texas', 'Utah', 'California']
frame3 = frame.reindex(columns=states)
print(frame3)
Output: 
   Texas Utah California
a  1     NaN    2
c  4     NaN    5
d  7     NaN    8
```

<h3 id="2">2. 删除指定数据drop</h4>
pandas中删除指定数据很简单，只要有一个索引数组或列表即可。由于需要执行一些数据整理和集合逻辑，所以drop方法<u>返回的是一个在指定轴上删除了指定值的新对象</u>：

```python
obj = pd.Series(np.arange(5.), index=['a', 'b', 'c', 'd', 'e'])
print(obj)
Output: 
a  0.0
b  1.0
c  2.0
d  3.0
e  4.0
dtype: float64

new_obj = obj.drop('c')
print(new_obj)
Output: 
a  0.0
b  1.0
d  3.0
e  4.0
dtype: float64

# 也可以删除多个索引对应的数据
new_new_obj = obj.drop(['d', 'c'])
print(new_new_obj)
Output: 
a   0.0
b   1.0
e   4.0
dtype: float64
```
对于DataFrame，可以删除任意轴上的索引值。为了演示，先新建一个DataFrame例子：
```python
import pandas as pd
import numpy as np

data = pd.DataFrame(np.arange(16).reshape((4, 4)), index = ['Ohio', 'Colorado', 'Utah', 'New York'], columns=['one', 'two', 'three', 'four'])
print(data)
Output: 
          one two three four
Ohio      0   1   2     3
Colorado  4   5   6     7
Utah      8   9   10    11
New York  12  13  14    15
```
用标签序列调用`drop`默认会从行标签(axis=0)删除值:
```python
data1 = data.drop(['Colorado', 'Ohio'])
print(data1)
Output: 
         one two three four
Utah     8   9   10    11
New York 12  13  14    15
```
通过传递axis=1或axis='columns'可以删除列的值：
```python
data2 = data.drop(['two', 'four'], axis = 1) # axis=1换成axis="columns"也可以
print(data2)
Output:
         one three
Ohio     0   2
Colorado 4   6
Utah     8   10
New York 12  14
```
许多函数，如drop，会修改Series或DataFrame的大小或形状，可以就地修改对象，不会返回新的对象:
```python
obj.drop('c', inplace=True) # 此时drop不再有返回值, 会对自身进行修改, 但小心使用inplace，它会销毁所有被删除的数据，意为着原先的数据将不复存在。
print(obj)
Output: 
a   0.0
b   1.0
d   3.0
e   4.0
dtype: float64
```
<h3 id=3>03 索引和切片</h3>
Series索引（obj[...]）的工作方式类似于NumPy数组的索引，只不过Series的索引值不只是整数。下面是几个例子：

```python
obj = pd.Series(np.arange(4.), index=['a', 'b', 'c', 'd'])
print(obj)
Output: 
a  0.0
b  1.0
c  2.0
d  3.0
dtype: float64

print(obj['b'])
Output: 1.0

# 也可以像列表那样进行索引
print(obj[1])
Output: 1

print(obj[2:4])
Output:
c   2.0
d   3.0
dtype: float64

print(obj[['b', 'a', 'd']])
Output:
b   1.0
a   0.0
d   3.0
dtype: float64
```
利用标签的切片运算与普通的Python切片运算不同，其末端是包含的：
```python
print(obj['b':'c'])
Output:
b   1.0
c   2.0
dtype: float64
```
用切片可以对Series的相应部分进行设置：
```python
obj['b', 'c'] = 5
print(obj)
Output:
a   0.0
b   5.0
c   5.0
d   3.0
dtype: float64
```
用一个值或序列对DataFrame进行索引其实就是获取一个或多个列：
```python
data = pd.DataFrame(np.arange(16).reshape((4, 4)),
index=['Ohio', 'Colorado', 'Utah', 'New York'],
columns=['one', 'two', 'three', 'four'])
print(data)
Output: 
         one two three four
Ohio     0   1   2     3
Colorado 4   5   6     7
Utah     8   9   10    11
New York 12  13  14    15

print(data['two'])
Output:
Ohio     1
Colorado 5
Utah     9
New York 13
Name: two, dtype: int64

# 也可以同时选取多个列
print(data[['three', 'one']])
Output: 
         three one
Ohio     2     0
Colorado 6     4
Utah     10    8
New York 14    12
```
这种索引方式有几个特殊的情况。首先通过切片或布尔型数组选取数据：
```python
print(data[:2])
Output: 
         one two three four
Ohio     0   1   2     3
Colorado 4   5   6     7

# 布尔型数组索引
print(data[data['three'] > 5])
Output: # 因为在three那一列中只有Ohio对应的值小于等于5, 所以Ohio对应的那一行不用显示出来
         one two three four
Colorado 4   5   6     7
Utah     8   9   10    11
New York 12  13  14    15
```
选取行的语法data[:2]十分方便。向[ ]传递单一的元素或列表，就可选择列。
另一种用法是通过布尔型DataFrame（比如下面这个由标量比较运算得出的）进行索引：
```python
print(data < 5)
Output: 
         one   two   three  four
Ohio     True  True  True   True
Colorado True  False False  False
Utah     False False False  False
New York False False False  False
```
这使得DataFrame的语法与NumPy二维数组的语法很像。

<h3 id=4>04 用loc和iloc进行索引</h3>

对于DataFrame的行的标签索引，我引入了特殊的标签运算符`loc`和`iloc`。它们可以让你用类似NumPy的标记，使用<u>轴标签</u>（`loc`）或<u>整数索引</u>（`iloc`），从DataFrame选择行和列的子集。作为一个初步示例，让我们通过标签选择一行和多列：
```python
print(data.loc['Colorado', ['two', 'three']])
Output: 
two      5
three    6
Name: Colorado, dtype: int64
```
我们也可以使用iloc和整数进行选取：
```python
print(data.iloc[2, [3, 0, 1]])
Output:
four   11
one    8
two    9
Name: Utah, dtype: int64

# 如果只想指定index
print(data.iloc[2])
Output: 
one    8
two    9
three  10
four   11
Name: Utah, dtype: int64

# 如果想指定多个index与columns
print(data.iloc[[1, 2], [3, 0, 1]])
Output: 
          four one two
Colorado  7    0   5
Utah      11   8   9
```
