### 01 Numpy介绍
NumPy（Numerical Python的简称）是Python数值计算最重要的基础包。大多数提供科学计算的
包都是用NumPy的数组作为构建基础。

NumPy的部分功能如下：
1. ndarray，一个具有矢量算术运算和复杂广播能力的快速且节省空间的多维数组。
用于对整组数据进行快速运算的标准数学函数（无需编写循环）。
2. 用于读写磁盘数据的工具以及用于操作内存映射文件的工具。
线性代数、随机数生成以及傅里叶变换功能。
3. 用于集成由C、C++、Fortran等语言编写的代码的A C API。

由于NumPy提供了一个简单易用的C API，因此很容易将数据传递给由低级语言编写的外部库，外
部库也能以NumPy数组的形式将数据返回给Python。这个功能使Python成为一种包装
C/C++/Fortran历史代码库的选择，并使被包装库拥有一个动态的、易用的接口。

NumPy本身并没有提供多么高级的数据分析功能，理解NumPy数组以及面向数组的计算将有助于
你更加高效地使用诸如pandas之类的工具。因为NumPy是一个很大的题目，我会在附录A中介绍
更多NumPy高级功能，比如广播。

对于大部分数据分析应用而言，我最关注的功能主要集中在：
1. 用于数据整理和清理、子集构造和过滤、转换等快速的矢量化数组运算。
2. 常用的数组算法，如排序、唯一化、集合运算等。
3. 高效的描述统计和数据聚合/摘要运算。
4. 用于异构数据集的合并/连接运算的数据对齐和关系型数据运算。
5. 将条件逻辑表述为数组表达式（而不是带有if-elif-else分支的循环）。
6. 数据的分组运算（聚合、转换、函数应用等）。。

虽然NumPy提供了通用的数值数据处理的计算基础，但大多数读者可能还是想将pandas作为统计
和分析工作的基础，尤其是处理表格数据时。pandas还提供了一些NumPy所没有的领域特定的功
能，如时间序列处理等。

```t
笔记：Python的面向数组计算可以追溯到1995年，Jim Hugunin创建了Numeric库。接下来
的10年，许多科学编程社区纷纷开始使用Python的数组编程，但是进入21世纪，库的生态系
统变得碎片化了。2005年，Travis Oliphant从Numeric和Numarray项目整了出了NumPy项
目，进而所有社区都集合到了这个框架下。
```
NumPy之于数值计算特别重要的原因之一，是因为它可以高效处理大数组的数据。这是因为：
NumPy是在一个连续的内存块中存储数据，独立于其他Python内置对象。NumPy的C语言编
写的算法库可以操作内存，而不必进行类型检查或其它前期工作。比起Python的内置序列，
NumPy数组使用的内存更少。

NumPy可以在整个数组上执行复杂的计算，而不需要Python的for循环。
要搞明白具体的性能差距，考察一个包含一百万整数的数组，和一个等价的Python列表：
```python
import numpy as np

my_arr = np.arange(1000000)

my_list = list(range(1000000))
```
各个序列分别乘以2:
```python
In [10]: %time for _ in range(10): my_arr2 = my_arr * 2
CPU times: user 20 ms, sys: 50 ms, total: 70 ms
Wall time: 72.4 ms
In [11]: %time for _ in range(10): my_list2 = [x * 2 for x in my_list]
CPU times: user 760 ms, sys: 290 ms, total: 1.05 s
Wall time: 1.05 s
```
基于NumPy的算法要比纯Python快10到100倍(甚至更快), 并且使用的内存更少。