### 11. collections-deque双向队列
双端队列，可以快速的从另外一侧追加和推出对象,`deque`是一个双向链表，针对`list`连续的数据结构插入和删除进行优化。它提供了两端都可以操作的序列，这表示在序列的前后你都可以执行添加或删除操作。双向队列(`deque`)对象支持以下方法：

#### 1. append(x)
添加x到双向队列的右端
```python
from collections import deque
d = deque('world')
d.append('j')
d
Output: deque(['w', 'o', 'r', 'l', 'd', 'j'])
```

#### 2. appendleft(x)
添加x到双向队列的左端
```python
d.appendleft('o')
d
Output: deque(['o', 'w', 'o', 'r', 'l', 'd', 'j'])
```
#### 3. clear()
移除双向队列内的所有元素, 使其长度为0.
```python
d.clear()
d
Output: deque([])
```

#### 4. copy()
创建一份拷贝
```python
d = deque('helloworld')
y = d.copy()
y
Output: deque(['h', 'e', 'l', 'l', 'o', 'w', 'o', 'r', 'l', 'd'])
```

#### 5. count(x)
计算双向队列中元素等于x的个数
```python
d = deque('abbcd')
d.count('b')
Ouput: 2
```

#### 6.extend
扩展双向队列的右侧, 通过添加`iterable`参数中的元素, 人话: 合并两个双向队列
```python
a = deque('abc')
b = deque('cd')
a.extend(b)
a
Output: deque(['a', 'b', 'c', 'c', 'd'])

#与append 的区别
a = deque('abc')
b = deque('cd')
a.append(b)
Output: deque(['a', 'b', 'c', deque(['c', 'd'])])
```

#### 7. extendleft()
扩展`deque`的左侧，通过添加`iterable`参数中的元素。注意，左添加时，在结果中`iterable`参数中的顺序将被反过来添加。
```python
a = deque('abc')
b = deque('cd')
a.extendleft(b)
a
Output: deque(['d', 'c', 'a', 'b', 'c'])
```

#### 8. index(x)
返回 x 在 deque 中的位置（在索引 start 之后，索引 stop 之前）。 返回第一个匹配项，如果未找到则引发 ValueError。
```python
d = deque('helloworld')
d.index(w)
Output: 5
```

#### 9.insert(index, value)
在位置 i 插入 x 。
如果插入会导致一个限长 deque 超出长度 maxlen 的话，就引发一个 IndexError。
```python
a = deque('abc')
a.insert(1,'X')
Output: deque(['a', 'X', 'b', 'c'])
```

#### 10. pop()
移去并且返回一个元素，deque 最右侧的那一个。 如果没有元素的话，就引发一个 IndexError。
```python
a.pop()
Output: 'c'
```

#### 11. popleft()
移去并且返回一个元素，deque 最左侧的那一个。 如果没有元素的话，就引发 IndexError。
```python
a.popleft()
Output: 'a'
```

#### 12. remove(value)
移除找到的第一个 value。 如果没有的话就引发 ValueError。
```python
a = deque('abca')
a.remove('a')
a
Output: deque(['b', 'c', 'a'])
```

#### 13. reverse()
将deque逆序排列, 无返回值
```python
d = deque('abc')
d.reverse()
d
Output: deque(['c', 'b', 'a'])
```

#### 14. rotate(n=1)
向右循环移动 n 步。 如果 n 是负数，就向左循环。
如果deque不是空的，向右循环移动一步就等价于 d.appendleft(d.pop()) ， 向左循环一步就等价于 d.append(d.popleft()) 。
```python
# 向右边挤一挤
d = deque('ghijkl')
d.rotate(1)                      
d
deque(['l', 'g', 'h', 'i', 'j', 'k'])

# 向左边挤一挤
d.rotate(-1)                     
d
deque(['g', 'h', 'i', 'j', 'k', 'l'])

#看一个更明显的
x = deque('12345')
x
deque(['1', '2', '3', '4', '5'])
x.rotate()
x
deque(['5', '1', '2', '3', '4'])

d = deque(['12','av','cd'])
d.rotate(1)
deque(['cd', '12', 'av'])
```

#### 15.maxlen参数
双向队列的最大尺寸，如果没有限定的话就是 None 。
```python
from collections import deque
d=deque(maxlen=10)
for i in range(20):
   d.append(i)
d  
deque([10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
```

除了以上操作，deque还支持`迭代`、封存、`len(d)`、`reversed(d)`、`copy.deepcopy(d)`、`copy.copy(d)`、成员检测运算符 in 以及下标引用例如通过 d[0] 访问首个元素等。 索引访问在两端的复杂度均为 O(1) 但在中间则会低至 O(n)。 如需快速随机访问，请改用列表。

Deque从版本3.5开始支持 __add__(), __mul__(), 和 __imul__() 。
