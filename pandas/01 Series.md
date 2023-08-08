### 01. Series
要使用`pandas`，你首先就得熟悉它的两个主要数据结构：`Series`和`DataFrame`。虽然它们并不能解决所有问题，但它们为大多数应用提供了一种可靠的、易于使用的基础。

**Series**

`Series`是一种类似于一维数组的对象，它由一组数据（各种`NumPy`数据类型）以及一组与之相关
的数据标签（即索引）组成。仅由一组数据即可产生最简单的`Series`：
```python
import pandas as pd

obj = pd.Series([4, 7, -5, 3])
print(obj)

Output:
0   4
1   7
2   -5
3   3
dtype: int64
```
Series的字符串表现形式为：**索引在左边，值在右边**。由于我们没有为数据指定索引，于是会自动创建一个0到N-1（N为数据的长度）的整数型索引。你可以通过Series 的`values`和`index`属性获取其数组表示形式和索引对象：
```python
print(obj.values)
Output: array([4, 7, -5, 3])

print(obj.index)
Output: RangeIndex(start=0, stop=4, step=1)
```
通常， 我们希望所创建的`Series`带有一个可以对各个数据点进行标记的索引:
```python
obj2 = pd.Series([4, 7, -5, 3], index = ['d', 'b', 'a', 'c']) 
print(obj2)

Output: 
d   4
b   7
a   -5
c   3
dtype: int64
```
与普通NumPy数组相比，你可以通过**索引**的方式选取Series中的单个或一组值：
```python
print(obj['a'])
Ouptut: -5

obj2['d'] = 6
print(obj2['c', 'a', 'd'])
Output:
c   3
a   -5
d   6
dtype: int64
```
['c', 'a', 'd']是索引列表，即使它包含的是字符串而不是整数。
使用NumPy函数或类似NumPy的运算（如根据布尔型数组进行过滤、标量乘法、应用数学函数等）都会保留索引值的链接：
```python
print(obj2[obj2>2])
Output:
d   6
b   7
c   3
dtype: int64

obj2 * 2
Output: 
d   12
b   14
a   -10
c   6
dtype: int64
```
还可以将Series看成是一个定长的**有序字典**，因为它是索引值到数据值的一个映射。它可以用在许多原本需要字典参数的函数中：
```python
print('b' in obj2)
Output: True

print('e' in obj2)
Output: False
```
如果数据被存放在一个Python字典中，也可以直接通过这个字典来创建Series：
```python
sdata = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}
obj3 = pd.Series(sdata)
print(obj3)
Output: 
Ohio    35000
Oregon  16000
Texas   71000
Utah    5000
dtype: int64
```
如果只传入一个字典，则结果Series中的索引就是原字典的键（有序排列）。你可以传入排好序的字典的键以改变顺序：
```python
states = ['California', 'Ohio', 'Oregon', 'Texas']
obj4 = pd.Series(sdata, index=states)
print(obj4)
output: 
California  NaN
Ohio        35000.0
Oregon      16000.0
Texas       71000.0
dtype: float64
```
在这个例子中，sdata中跟states索引相匹配的那3个值会被找出来并放到相应的位置上，但由于"California"所对应的sdata值找不到，所以其结果就为`NaN`（即“非数字”（not a number），在pandas中，它用于表示缺失或NA值）。因为‘Utah’不在states中，它被从结果中除去。

我们将使用缺失（missing）或NA表示缺失数据。pandas的isnull和notnull函数可用于检测缺失数据：
```python
print(pd.isnull(obj4))
Output: 
California  True
Ohio        False
Oregon      False
Texas       False
dtype: bool

# 与isnull函数对应的还有notnull()函数
print(pd.notnull(obj4))
Output: 
California  False
Ohio        True
Oregon      True
Texas       True
dtype: bool
```
对于许多应用而言，Series最重要的一个功能是，**它会根据运算的索引标签自动对齐数据**：
```python
print(obj3)
Output:
Ohio    35000
Oregon  16000
Texas   71000
Utah    5000
dtype: int64

print(obj4)
Output:
California  NaN
Ohio        35000.0
Oregon      16000.0
Texas       71000.0
dtype: float64

print(obj3 + obj4)
Output: 
California  NaN
Ohio        70000.0
Oregon      32000.0
Texas       142000.0
Utah        NaN
dtype: float64
```
Series对象本身及其索引都有一个name属性，该属性跟pandas其他的关键功能关系非常密切：
```python
obj4.name = 'population'
obj4.index.name = 'state'
print(obj4)
Output:
state
California  NaN
Ohio        35000.0
Oregon      16000.0
Texas       71000.0
Name: population, dtype: float64
```
Series的索引可以通过赋值的方式就地修改：
```python
print(obj)
Output: 
0   4
1   7
2   -5
3   3
dtype:int64

obj.index = ['a', 'b', 'c', 'd']
print(obj)
Output:
a   4
b   7
c   -5
d   3
dtype: int64
```
