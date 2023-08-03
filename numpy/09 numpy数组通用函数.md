### 09. numpy数组通用函数
通用函数（即`ufunc`）是一种对`ndarray`中的数据执行元素级运算的函数。你可以将其看做简单函数
（接受一个或多个标量值，并产生一个或多个标量值）的矢量化包装器。
许多`ufunc`都是简单的元素级变体，如`sqrt`和`exp`：
```python
arr = np.arange(10)
arr
Output: array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

np.sqrt(arr)
Output: array([ 0. , 1. , 1.4142, 1.7321, 2. , 2.2361, 2.4495,
2.6458, 2.8284, 3. ])

np.exp(arr)
Output: array([ 1. , 2.7183, 7.3891, 20.0855, 54.5982,
148.4132, 403.4288, 1096.6332, 2980.958 , 8103.0839])
```
这些都是一元（unary）`ufunc`。另外一些（如add或maximum）接受`2`个数组（因此也叫二元
（binary）ufunc），并返回一个结果数组：
```python
 x = np.random.randn(8)
 y = np.random.randn(8)

x
Output: array([-0.0119, 1.0048, 1.3272, -0.9193, -1.5491, 0.0222, 0.7584,
-0.6605])

y 
Output: array([ 0.8626, -0.01 , 0.05 , 0.6702, 0.853 , -0.9559, -0.0235,
-2.3042])

np.maximum(x, y)
Output: array([ 0.8626, 1.0048, 1.3272, 0.6702, 0.853 , 0.0222, 0.7584,
-0.6605])
```
这里，`numpy.maximum`计算了`x`和`y`中元素级别最大的元素。

#### 一元通用函数

|函数名|	描述|
|------|--------|
|abs、fabs	|逐个元素地计算整数、浮点数或复数地绝对值
|sqrt	|计算每个元素的平方根(与arr ** 0.5相等)
|square	|计算每个元素地平方(与arr ** 2相等)
|exp	|计算每个元素的自然指数值e^x次方
|log、log10、log2、log1p	|分别对应(自然指数(e为底)、对数10为底、对数2为底、log(1+x))
|sign	|计算每个元素的符号值：1(正数)、0(0)、-1(负数)
|ceil	|计算每个元素的最高整数值(即大于等于给定数值的最小整数)
|floor	|计算每个元素的最小整数值(即小于等于给定整数的最大整数)
|rint	|将元素保留到整数位，并保持dtype
|modf	|分别将数组的小数部分与整数部分按数组形式返回
|isnan	|返回数组元素是否是一个NaN(非数值)，形式为布尔值数组
|isfinite、isinf	|分别返回数组中的元素是否有限(非inf、非NaN)、是否无限的，形式为布尔值数组
|cos、cish、sin、sinh、tan、tanh|	常规三角函数及双曲三角函数
|arccos、arccosh、arcsin、arcsinh、arctan、arctanh	|反三角函数
|logical_not	|对数组元素按位取反

#### 二元通用函数
|函数名	|描述
|------|----|
|add	|将数组的对应元素相加
|subtract	|在第二个数组中，将第一个数组中包含的元素去除
|multiply	|将数组的对应元素相乘
|divide,floor_divide	|除或整除(放弃余数)
|power	|将第二个数组的元素作为第一个数组对应元素的幂次方
|maximum	|逐个元素计算最大值，fmax忽略NaN
|minimum	|逐个元素计算最小值，fmin忽略NaN
|mod	|按元素的求模计算(即求除法的余数)
|copysign	|将第一个数组的符号值改为第二个数组的符号值
|greater,greater_equal,less，less_equal,equal,not_equal		|进行逐个元素的比较，返回布尔值数组（与数学操作符>,>=,<,<=,==,!=x效果一致）
|logical_and,logical_or	|进行逐个元素的逻辑操作(与逻辑操作符&、丨、^效果一致)
|logical_xor	| 按位异或


