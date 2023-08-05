### 09. collections模块介绍
#### 1. 模块作用
官方说法：`collections`模块实现了特定目标的容器，以提供Python标准内建容器`dict` ,`list` , `set` , 和`tuple`的替代选择。

通俗说法：Python内置的数据类型和方法，`collections`模块在这些内置类型的基础提供了额外的高性能数据类型，比如基础的字典是不支持顺序的，`collections`模块的`OrderedDict`类构建的字典可以支持顺序，collections模块的这些扩展的类用处非常大，熟练掌握该模块，可以大大简化Python代码，提高Python代码逼格和效率，高手入门必备。

用collections.__all__查看所有的子类，一共包含9个
```python
import collections
print(collections.__all__)
Output: ['deque', 'defaultdict', 'namedtuple', 'UserDict', 'UserList', 
'UserString', 'Counter', 'OrderedDict', 'ChainMap']
```

这个模块实现了特定目标的容器，以提供`Python`标准内建容器`dict` , `list` , `set` , 和`tuple` 的替代选择。

|namedtuple()  |创建命名元组子类的工厂函数，生成可以使用名字来访问元素内容的tuple子类   |
|--|---|
|deque  |类似列表(list)的容器，实现了在两端快速添加(append)和弹出(pop)   |
|ChainMap  |类似字典(dict)的容器类，将多个映射集合到一个视图里面   |
|Counter  |字典的子类，提供了可哈希对象的计数功能   |
|OrderedDict  |字典的子类，保存了他们被添加的顺序，有序字典   |
|defaultdict  |字典的子类，提供了一个工厂函数，为字典查询提供一个默认值   |
|UserDict|封装了字典对象，简化了字典子类化|
|UserList|封装了列表对象，简化了列表子类化|
|UserString|封装了字符串对象，简化了字符串子类化|