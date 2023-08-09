### 02. DataFrame
`DataFrame`是一个表格型的数据结构，它含有一组有序的列，每列可以是不同的值类型（数值、字符串、布尔值等）。`DataFrame`既有行索引也有列索引，它可以被看做由`Series`组成的字典（共用同一个索引）。`DataFrame`中的数据是以一个或多个二维块存放的（而不是列表、字典或别的一维数据结构）。有关`DataFrame`内部的技术细节远远超出了本书所讨论的范围。
创建`DataFrame`的办法有很多, 最常用的一种是直接传入一个由等长列表或`NumPy`数组组成的字典:
```python
import pandas as pd
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
'year': [2000, 2001, 2002, 2001, 2002, 2003],
'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}
frame = pd.DataFrame(data)
```
结果DataFrame会自动加上索引（跟Series一样），且全部列会被有序排列：
```python
print(frame)
Output: 
    pop   state  year
0   1.5   Ohio   2000
1   1.7   Ohio   2001
2   3.6   Ohio   2002
3   2.4   Nevada 2001
4   2.9   Nevada 2002
5   3.2   Nevada 2003
```
如果你使用的是`Jupyter notebook`，`pandas DataFrame`对象会以对浏览器友好的HTML表格的方式呈现。
对于特别大的DataFrame, head方法会选取前五行:
```python
print(frame.head())
Output: 
    pop   state  year
0   1.5   Ohio   2000
1   1.7   Ohio   2001
2   3.6   Ohio   2002
3   2.4   Nevada 2001
4   2.9   Nevada 2002
```
如果指定了列序列，则DataFrame的列就会按照指定顺序进行排列：
```python
frame = pd.DataFrame(data, columns = ['year', 'state', 'pop'])
print(frame)
Output: 
  year  state   pop
0 2000  Ohio    1.5
1 2001  Ohio    1.7
2 2002  Ohio    3.6
3 2001  Nevada  2.4
4 2002  Nevada  2.9
5 2003  Nevada  3.2
```
如果传入的列在数据中找不到, 就会在结果中产生缺失值:
```python
frame2 = pd.DataFrame(data, columns=['year', 'state', 'pop', 'debt'],
index=['one', 'two', 'three', 'four', 'five', 'six'])
print(frame2)
Output: 
      year  state  pop  debt
one   2000  Ohio   1.5  NaN
two   2001  Ohio   1.7  NaN
three 2002  Ohio   3.6  NaN
four  2001  Nevada 2.4  NaN
five  2002  Nevada 2.9  NaN
six   2003  Nevada 3.2  NaN

print(frame2.columns)
Output: Index(['year', 'state', 'pop', 'debt'], dtype='object')
```
通过类似字典标记的方式或属性的方式, 
```python
# 两种方法
# 第一种字典索引方法
print(frame2['state'])
Output: 
one     Ohio
two     Ohio
three   Ohio
four    Nevada
five    Nevada
six     Nevada
Name: state, dtype: object

# 第二种索引方法
print(frame.year)
Output: 
one     2000
two     2001
three   2002
four    2001
five    2002
six     2003
Name: year, dtype: int64
```
注意，返回的Series拥有原DataFrame相同的索引，且其name属性也已经被相应地设置好了。行也可以通过位置或名称的方式进行获取，比如用`loc`属性（稍后将对此进行详细讲解）：
```python
# 获取DataFrame的行
print(frame2.loc['three'])
Output: 
year    2002
state   Ohio
pop     3.6
debt    NaN
Name: three, dtype: object
```
列可以通过赋值的方式进行修改。例如，我们可以给那个空的"debt"列赋上一个标量值或一组值：
```python
frame2['debt'] = 16.5
print(frame)
Output: 
       year   state  pop  debt
one    2000   Ohio   1.5  16.5
two    2001   Ohio   1.7  16.5
three  2002   Ohio   3.6  16.5
four   2001   Nevada 2.4  16.5
five   2002   Nevada 2.9  16.5
six    2003   Nevada 3.2  16.5

frame['debt'] = np.arange(6.)
print(frame2)
Output:
      year  state  pop  debt
one   2000  Ohio   1.5  0.0
two   2001  Ohio   1.7  1.0
three 2002  Ohio   3.6  2.0
four  2001  Nevada 2.4  3.0
five  2002  Nevada 2.9  4.0
six   2003  Nevada 3.2  5.0
```
将列表或数组赋值给某个列时，其长度必须跟DataFrame的长度相匹配。如果赋值的是一个`Series`，就会精确匹配DataFrame的索引，所有的空位都将被填上缺失值：
```python
val = pd.Series([-1.2, -1.5, -1.7], index=['two', 'four', 'five'])
frame2['debt'] = val
print(frame2)
Output: 
      year  state  pop  debt
one   2000  Ohio   1.5  NaN
two   2001  Ohio   1.7  -1.2
three 2002  Ohio   3.6  NaN
four  2001  Nevada 2.4  -1.5
five  2002  Nevada 2.9  -1.7
six   2003  Nevada 3.2  NaN
```
为不存在的列赋值会创建出一个新列。关键字del用于删除列。作为del的例子，我先添加一个新的布尔值的列，state是否为'Ohio'：
```python
frame2['eastern'] = frame2.state == 'Ohio'
print(frame2)
Output:
      year  state  pop  debt eastern
one   2000  Ohio   1.5  NaN  True
two   2001  Ohio   1.7  -1.2 True
three 2002  Ohio   3.6  NaN  True
four  2001  Nevada 2.4  -1.5 False
five  2002  Nevada 2.9  -1.7 False
six   2003  Nevada 3.2  NaN  False
```
del方法可以用来删除这列
```python
del frame2['eastern']
print(frame.columns)
Output: Index(['year', 'state', 'pop', 'debt'], dtype='object') # 注意eastern列没了
```
另一种常见的数据形式是嵌套字典：
```python
pop = {'Nevada': {2001: 2.4, 2002: 2.9},
 'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}
```
如果嵌套字典传给DataFrame，pandas就会被解释为：**外层字典的键作为列**，内层键则作为行索引：
```python
frame3 = pd.DataFrame(pop)
print(frame3)
Output: 
      Nevada Ohio
2000  NaN    1.5
2001  2.4    1.7
2002  2.9    3.6
```
内层字典的键会被合并、排序以形成最终的索引。如果明确指定了索引，则不会这样：
```python
print(pd.DataFrame(pop, index=[2001, 2002, 2003]))
Output:
     Nevada Ohio
2001 2.4    1.7
2002 2.9    3.6
2003 NaN    NaN
```
由Series组成的字典差不多也是一样的用法：
```python
pdata = {'Ohio': frame3['Ohio'][:-1],
 'Nevada': frame3['Nevada'][:2]}
print(pd.DataFrame(pdata))
Output:
      Nevada Ohio
2000  NaN    1.5
2001  2.4    1.7
```
下表列出了DataFrame构造函数所能接受的各种数据
<img src = "../image/dataframe1.png"></img>
如果设置了DataFrame的index和columns的name属性, 则这些信息也会被显示出来:

```python
frame3.index.name = 'year'
frame3.columns.name = 'state'
print(frame3)
Output: 
state Nevada Ohio
year
2000  NaN    1.5
2001  2.4    1.7
2002  2.9    3.6
```
跟Series一样，`values`属性也会以二维`ndarray`的形式返回`DataFrame`中的数据：
```python
print(frame3.values)
Output: 
array([[ nan, 1.5],
        [ 2.4, 1.7],
        [ 2.9, 3.6]])
```
如果DataFrame各列的数据类型不同，则值数组的dtype就会选用能兼容所有列的数据类型：
```python
print(frame2.values)
Output: 
array([[2000, 'Ohio', 1.5, nan],
        [2001, 'Ohio', 1.7, -1.2],
        [2002, 'Ohio', 3.6, nan],
        [2001, 'Nevada', 2.4, -1.5],
        [2002, 'Nevada', 2.9, -1.7],
        [2003, 'Nevada', 3.2, nan]], dtype=object)
```