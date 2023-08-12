### 03 pandas的索引
pandas的索引对象负责管理轴标签和其他元数据（比如轴名称等）。构建`Series`或`DataFrame`时，所用到的任何数组或其他序列的标签都会被转换成一个`Index`:

```python
obj = pd.Series(range(3), index = ['a', 'b', 'c'])
index = obj.index
print(index)
Output: Index(['a', 'b', 'c'], dtype='object')

# 对于索引我们也可以进行切片操作
print(index[1:])
Output: Index(['b', 'c'], dtype='object')
```

但是Index对象是不可变的, 因此用户不能对其进行修改

```python
index[1] = 'd' # 会报错TypeError
```
不可变可以是Index对象在多个数据结构之间安全共享

```python
labels = pd.Index(np.arange(3))
print(labels)
Output: Int64Index([0, 1, 2], dtype='int64')

obj2 = pd.Series([1.5, -2.5, 0], index = labels)
print(obj2)
Output:
0   1.5
1   -2.5
2   0.0
dtype: float64
```
**注意**：<u>虽然用户不需要经常使用`Index`的功能，但是因为一些操作会生成包含被索引化的数据，理解它们的工作原理是很重要的。</u>
除了类似于数组，`Index`的功能也类似一个固定大小的集合：
```python
print(frame3)
Output:
state  Nevada  Ohio
year
2000   NaN     1.5
2001   2.4     1.7
2002   2.9     3.6

print(frame3.columns)
Output: Index(['Nevada', 'Ohio'], dtype='object', name = 'state')

print(frame3.index)
Output: Index([2000, 2001, 2002], dtype='object', name = 'year')
```
每个索引都有一些方法和属性，它们可用于设置逻辑并回答有关该索引所包含的数据的常见问题。下表列出了这些函数。
|方法|说明|
|---|-----|
|append|连接另一个Index对象, 产生一个新的Index|
|difference|计算差集, 并得到一个Index|
|intersection|计算交集|
|union|计算并集|
|isin|计算一个指示各值是否都包含在参数集合的布尔型数组|
|delete|删除索引i处的元素，得到新的Index|
|drop|删除传入的值，并得到新的Index|
|insert|将元素插入到索引i处，得到新的Index|
|unique|计算Index中唯一值的数组|
|is_unique|当Index没有重复值时， 返回True|
|is_monotonic|当各元素均大于等于前一个元素时， 返回True|

```python
import pandas as pd

index1 = pd.Index([1, 2, 3, 4, 5])
index2 = pd.Index([1, 5, 2, 9, 10])

# append函数
index3 = index1.append(index2)
print(index1)
Output: Index([1, 2, 3, 4, 5, 1, 5, 2, 9, 10], dtype='int64')

# difference函数
index4 = index1.difference(index2) # 返回存在在index1中的元素并且不存在index2中的元素， 然后返回成一个Index对象
print(index4)
Output: Index([3, 4], dtype='int64')

# intersection函数
index5 = index1.intersection(index2)
print(index5)
Output: Index([1, 2, 5], dtype = 'int64')

# union函数
index6 = index1.union(index2)
print(index6)
Output: Index([1, 2, 3, 4, 5, 9, 10], dtype='int64')

#isin函数
index7 = index1.isin([1, 2, 3, 3, 3])
print(index7)
Output: [True, True, True, False, False]

# delete函数
index8 = index1.delete(1)
print(index8)
Output: Index([1, 3, 4, 5], dtype = 'int64')

# drop函数
index9 = index1.drop(5)
print(index9)
Output: Index([1, 2, 3, 4], dtype = 'int64')

# insert函数
index10 = index1.insert(2, 11)
print(index10)
Output: Index([1, 2, 10, 3, 4, 5], dtype='int64')

# 后面的函数可以自己试试效果
```