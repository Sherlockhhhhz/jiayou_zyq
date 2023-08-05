### 10. collections-Counter计数器
一个计数器工具提供快速和方便的计数，`Counter`是一个`dict`的子类，用于计数可哈希对象。它是一个集合，元素像字典键(`key`)一样存储，它们的计数存储为值。计数可以是任何整数值，包括0和负数，Counter类有点像其他语言中的bags或multisets。简单说，就是可以统计计数，来几个例子看看就清楚了，比如
```python
from collections import Counter
import re

text = 'remove an existing key one level down remove an existing key one level down'
#计算列表中单词的个数
cnt = Counter()
for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
    cnt[word] += 1
cnt
Output: Counter({'red': 2, 'blue': 3, 'green': 1})words = re,find

#上述这样计算有点嘛，下面的方法更简单，直接计算就行
L = ['red', 'blue', 'red', 'green', 'blue', 'blue'] 
Counter(L)
Counter({'red': 2, 'blue': 3, 'green': 1})
```
元素从一个`iterable` 被计数或从其他的`mapping` (or counter)初始化：
```python
from collections import Counter

#字符串计数
Counter('gallahad') 
Output: Counter({'g': 1, 'a': 3, 'l': 2, 'h': 1, 'd': 1})

#字典计数
Counter({'red': 4, 'blue': 2})  
Output: Counter({'red': 4, 'blue': 2})

#是个啥玩意计数
Counter(cats=4, dogs=8)
Output: Counter({'cats': 4, 'dogs': 8})

Counter(['red', 'blue', 'red', 'green', 'blue', 'blue'])
Output: Counter({'red': 2, 'blue': 3, 'green': 1})
```
计数器对象除了字典方法以外，还提供了三个其他的方法：
#### 1. elements()
**描述**：返回一个迭代器，其中每个元素将重复出现计数值所指定次。 元素会按首次出现的顺序返回。 如果一个元素的计数值小于1，elements() 将会忽略它, **没有参数**。
```python
c = Counter(a=4, b=2, c=0, d=-2)
Output: list(c.elements())
['a', 'a', 'a', 'a', 'b', 'b']

sorted(c.elements())
Output: ['a', 'a', 'a', 'a', 'b', 'b']

c = Counter(a=4, b=2, c=0, d=5)
list(c.elements())
Output: ['a', 'a', 'a', 'a', 'b', 'b', 'd', 'd', 'd', 'd', 'd']
```

#### 2. most_common()
返回一个列表，其中包含n个最常见的元素及出现次数，按常见程度由高到低排序。 如果 n 被省略或为None，most_common() 将返回计数器中的所有元素，计数值相等的元素按首次出现的顺序排序，经常用来计算top词频的词语。
```python
Counter('abracadabra').most_common(3)
Output: [('a', 5), ('b', 2), ('r', 2)]

Counter('abracadabra').most_common(5)
Output: [('a', 5), ('b', 2), ('r', 2), ('c', 1), ('d', 1)]
```
#### 3. subtract()
从迭代对象或映射对象**减去**元素。像`dict.update()` 但是是减去，而不是替换。输入和输出都可以是0或者负数。
```python
c = Counter(a=4, b=2, c=0, d=-2)
d = Counter(a=1, b=2, c=3, d=4)
c.subtract(d)
c
Output: Counter({'a': 3, 'b': 0, 'c': -3, 'd': -6})

#减去一个abcd
str0 = Counter('aabbccdde')
str0
Output: Counter({'a': 2, 'b': 2, 'c': 2, 'd': 2, 'e': 1})

str0.subtract('abcd')
str0
Output: Counter({'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1})
```
#### 字典方法
通常字典方法都可用于Counter对象，除了有两个方法工作方式与字典并不相同。

`fromkeys(iterable)`

这个类方法没有在Counter中实现。

`update([iterable-or-mapping])`

从迭代对象计数元素或者从另一个映射对象 (或计数器) 添加。 像 dict.update() 但是是加上，而不是替换。另外，迭代对象应该是序列元素，而不是一个 (key, value) 对。
```python
sum(c.values())                 # total of all counts
c.clear()                       # reset all counts
list(c)                         # list unique elements
set(c)                          # convert to a set
dict(c)                         # convert to a regular dictionary
c.items()                       # convert to a list of (elem, cnt) pairs
Counter(dict(list_of_pairs))    # convert from a list of (elem, cnt) pairs
c.most_common()[:-n-1:-1]       # n least common elements
+c                              # remove zero and negative counts
```
#### 数学操作
这个功能非常强大，提供了几个数学操作，可以结合 Counter 对象，以生产 multisets (计数器中大于0的元素）。 加和减，结合计数器，通过加上或者减去元素的相应计数。交集和并集返回相应计数的最小或最大值。每种操作都可以接受带符号的计数，但是输出会忽略掉结果为零或者小于零的计数)。
```python
c = Counter(a=3, b=1)
d = Counter(a=1, b=2)
c + d                       # add two counters together:  c[x] + d[x]
Output: Counter({'a': 4, 'b': 3})
c - d                       # subtract (keeping only positive counts)
Output: Counter({'a': 2})
c & d                       # intersection:  min(c[x], d[x]) 
Output: Counter({'a': 1, 'b': 1})
c | d                       # union:  max(c[x], d[x])
Output: Counter({'a': 3, 'b': 2})
```
单目加和减（一元操作符）意思是从空计数器加或者减去。
```python
c = Counter(a=2, b=-4)
+c
Output: Counter({'a': 2})
-c
Output: Counter({'b': 4})
```