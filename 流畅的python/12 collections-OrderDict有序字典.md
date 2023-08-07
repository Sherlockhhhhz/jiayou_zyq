### 12. collections-OrderDict有序字典
有序词典就像常规词典一样，但有一些与排序操作相关的额外功能,`popitem()` 方法有不同的签名。它接受一个可选参数来指定弹出哪个元素。`move_to_end()` 方法，可以有效地将元素移动到任一端。

有序词典就像常规词典一样，但有一些与排序操作相关的额外功能。由于内置的 dict 类获得了记住插入顺序的能力（在 Python 3.7 中保证了这种新行为），它们变得不那么重要了。

一些与 dict 的不同仍然存在：

常规的 `dict` 被设计为非常擅长映射操作。 跟踪插入顺序是次要的。
`OrderedDict` 旨在擅长重新排序操作。 空间效率、迭代速度和更新操作的性能是次要的。
算法上， `OrderedDict` 可以比 `dict` 更好地处理频繁的重新排序操作。 这使其适用于跟踪最近的访问（例如在 LRU cache 中）。
对于 `OrderedDict` ，相等操作检查匹配顺序。
OrderedDict 类的 popitem() 方法有不同的签名。它接受一个可选参数来指定弹出哪个元素。
OrderedDict 类有一个 move_to_end() 方法，可以有效地将元素移动到任一端。
Python 3.8之前， dict 缺少 `__reversed__()` 方法。

#### 1.popitem()
语法：`popitem(last=True)`

功能：有序字典的 popitem() 方法移除并返回一个 (key, value) 键值对。 如果 last 值为真，则按 LIFO 后进先出的顺序返回键值对，否则就按 FIFO 先进先出的顺序返回键值对。
```python
from collections import OrderedDict
d = OrderedDict.fromkeys('abcde')
d.popitem()
Output: ('e', None)

d
Output: OrderedDict([('a', None), ('b', None), ('c', None), ('d', None)])

#last=False时，弹出第一个
d = OrderedDict.fromkeys('abcde')
''.join(d.keys())
Output: 'abcde'

d.popitem(last=False)
''.join(d.keys())
Output: 'bcde'
```

#### 2. move_to_end()
```python
from collections import OrderedDict
d = OrderedDict.fromkeys('abcde')
d.move_to_end('b')
''.join(d.keys())
Output: 'acdeb'

d
Output: OrderedDict([('a', None), ('c', None), ('d', None), ('e', None), ('b', None)])


d.move_to_end('b', last=False)
''.join(d.keys())
Output: 'bacde'
```

