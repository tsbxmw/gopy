# Python  - 高级用法 - 数据模型（1）

> 本章将主要讲解 ```python 2 - 高级用法``` 系列的第二篇，```python 数据模型```。```python```这门语言，由于入门简单，使用方便，在近几年增长迅速。但也由于这个特点，导致很多没有编程基础的人，往往学得其形，而学不得其神。下面的内容，将基于```python doc```提供的数据模型章节进行分析，解析 ```python```中提供的数据模型。

由于此部分的知识与其他部分的叠加非常大，所以在本章中只会粗略的讲解一些基本的概念和实例。由于本部分的内容也相当多切杂，只能分为几章的内容进行说明。部分内容引自官网```doc```，有需要的可以直接移步官网查看[doc](https://docs.python.org/zh-cn/3/reference/datamodel.html)。

## 对象，值，类型

  ```对象```是```python```中对数据的抽象。万物皆对象，是```python```对所有类型的描述。而且，事实上```Python```中的所有数据都是由对象或对象间关系来表示的。

- 对象被创建后，它的 ```id``` 就不会改变了。查看一个对象的```id```，可以使用```id()```函数。

```python
>>> id(1)
4547570768
>>> id(0)
4547570736
```

- 查看两个对象是否是同一个对象的引用，实际上查看的就是对象的```id```，在```python```中存在一个内置函数```is```，可以实现上述功能。

```python
>>> a = 1
>>> b = 1
>>> a is b
True
```

- 查看一个对象的类型，则使用 ```type()```函数。与```id```一样，对象的类型也是不可变的。而且```tpye```函数返回的对象的类型也是一个对象。

```python
>>> a = 1
>>> type(a)
<class 'int'>
>>> type(1)
<class 'int'>
>>> type(type(1))
<class 'type'>
```

- 而对象的类型，据定了该对象支持的操作，并且定义了该对象的可能取值。

```python
>>> a = 1
>>> len(a)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: object of type 'int' has no len()
>>> b = []
>>> len(b)
0
```

- 使用 ```dir()```可以查看对象支持的操作。

```python
>>> dir(a)
['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
```


- 对象的类型定义了对象的可能取值。

- 值可以改变的对象既可变对象，值不可以改变的对象既不可变对象。

(一个不可变容器对象如果包含对可变对象的引用，当后者的值改变时，前者的值也会改变；但是该容器仍属于不可变对象，因为它所包含的对象集是不会改变的。因此，不可变并不严格等同于值不能改变，实际含义要更微妙。) 一个对象的可变性是由其类型决定的；例如，数字、字符串和元组是不可变的，而字典和列表是可变的。

- 对象绝不会被显示的销毁。就算引用被显示的```del```后，对象```1```还是存在的。

```python
>>> id(1)
4547570768
>>> a = 1
>>> id(a)
4547570768
>>> del a
>>> a
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'a' is not defined
>>> id(1)
4547570768
```

- 当对象无法访问时，可能会作为垃圾回收。此时需要参考```python gc```机制。

注意：类型会影响对象行为的几乎所有方面。甚至对象编号的重要性也在某种程度上受到影响: 对于不可变类型，会得出新值的运算实际上会返回对相同类型和取值的任一现有对象的引用，而对于可变类型来说这是不允许的。

> 例如在 a = 1; b = 1 之后，a 和 b 可能会也可能不会指向同一个值为一的对象，这取决于具体实现，但是在 c = []; d = [] 之后，c 和 d 保证会指向两个不同、单独的新建空列表。(请注意 c = d = [] 则是将同一个对象赋值给 c 和 d。)



## 内置类型

内置类型较多，我们只重点分析几个常用的类型。

### None

  ```None```既然是对象，那么它一定有```id```和类型。

```python
>>> type(None)
<class 'NoneType'>
>>> id(None)
4547268712
>>> None is None
True
```

它是```NoneType```类型，而且可以使用```is```操作比较。

来看一下它支持的操作。

```python
>>> dir(None)
['__bool__', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
```

没想到作为一个```None```，它竟然支持这么多操作。下面看下 ```bool```和```str```。

- bool

方法```__bool__```表示可以支持进行逻辑判断，而且```None```表示为 ```False```, 但是```None```并不是```False```,只有通过```bool```转换后它们才是相同的。调用```None.__bool__()```既```bool(None)```。

```python
>>> None.__bool__()
False
>>> bool(None)
False
>>> None is False
False
>>> None == False
False
>>> bool(None) == False
True
```

- str,repr

方法```__str__```和 ```__repr__```表示当调用```str(None)```时，调用的方法。

```python
>>> None.__str__()
'None'
>>> None.__repr__()
'None'
>>> str(None)
'None'
```

### 可调用类型

#### 用户调用函数

用户定义函数对象可通过函数定义来创建。它被调用时应附带一个参数列表，其中包含的条目应与函数所定义的形参列表一致。

**函数也是对象**,而且对象类型为 ```function```,可以查看函数的属性。

```python
>>> def test():
...     print(1)
...
>>> dir(test)
['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
>>> type(test)
<class 'function'>
>>> test.__name__
'test'
>>> str(test)
'<function test at 0x10f492b70>'
>>> test.__repr__()
'<function test at 0x10f492b70>'
```

- ```__closure__```

这里我们再来提一次```__closure__```属性，在装饰器那里我们说这个属性是用来实现```装饰器```的关键，用来存储于闭包相关的属性。

```python
>>> test.__closure__ is None
True
```

它的值为```None```或包含该函数可用变量的绑定的单元的元组。单元对象具有 ```cell_contents``` 属性。当我们尝试改变它的时候，```python```解释器会向我们抛出一个错误```AttributeError```。

```python
>>> test.__closure__ = test
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: readonly attribute
```

- ```__code__```

这里存储的是编译后的代码对象，类型为```code```。实际上的调用 ```test()``` 与 ```exec(test.__code__)``` 与 ```eval(test.__code__)```是相同的。

```python
>>> test.__code__
<code object test at 0x10f44c9c0, file "<stdin>", line 1>
>>> exec(test.__code__)
1
>>> eval(test.__code__)
1
```

- ```__module__```

当前函数所属的模块名称，这里建议先了解模块相关知识。

```python
>>> test.__module__
'__main__'
```

上面的代码是由于我们在```python```解释器中定义了```test```，所以所属的模块为```__main__```。


— ```__defaults__```

由具有默认值的参数的默认值组成的元组，没有默认参数为```None```。

这里我们定义了一个新的函数```test__para(a, b, c=1, d=None)```。

```python
>>> def test_para(a, b, c=1, d=None):
...     print(f"a={a}, b={b}, c={c}, d={d}")
>>> test_para(1, 2, 3, 4)
a=1, b=2, c=3, d=4

>>> test_para.__defaults__
(1, None)
```

所以它只存储了含有默认值的参数```c=1, d=None```的默认值，既```(1, None)```。


- ```__globals__```

存放的是一个全局变量字典```globals()```的引用。可以看到他们的```id```都是一样的，使用```is```判断的结果为 ```true```。

```python
>>> globals()
{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, 'b': [], 'a': None, 'test': <function test at 0x10f492b70>, 'builtins': <module 'builtins' (built-in)>, 'test_para': <function test_para at 0x10f4926a8>}
>>> test_para.__globals__
{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, 'b': [], 'a': None, 'test': <function test at 0x10f492b70>, 'builtins': <module 'builtins' (built-in)>, 'test_para': <function test_para at 0x10f4926a8>}

>>> test_para.__globals__ is globals()
True
```

- ```__annotations__```

参数标志是用来方便查看定义的对象的参数类型的，并不起到检测的作用。
包含参数标注的字典。字典的键是参数名，如存在返回标注则为 'return'。

这里我们重写了```test_para```函数，加入了对```c:str=1, d:int=None```的参数标志。

```python
>>> def test_para(a, b, c:str=1, d:int=None):
...     print(f"a={a}, b={b}, c={c}, d={d}")
...
>>> test_para(1,2,3,4)
a=1, b=2, c=3, d=4

>>> test_para.__annotations__
{'c': <class 'str'>, 'd': <class 'int'>}
```

可以看到参数标志存到了```__annotations__```中。

- ```__kwdefaults__```

存储了包含关键字默认值的字典。

这里我们重写了函数```test_para(a,b,*args,c:str=1,d:int=None)```。

```python
>>> def test_para(a, b, *args, c:str=1, d:int=None):
...     print(f"a={a}, b={b}, c={c}, d={d}")
>>> test_para(1,2,3,4,5)
a=1, b=2, c=1, d=None
>>> test_para.__kwdefaults__
{'c': 1, 'd': None}
```



#### 实例方法

实例方法用于结合类、类实例和任何可调用对象 (通常为用户定义函数)。

这个描述，官方文档写的相当复杂，我们结合例子看下。

```python
>>> class Tclass(object):
...      def test(self, a):
...          print(a)
...
>>> t = Tclass()
>>> t.test(1)
1
>>> Tclass.test(t, 1)
1
```

想要表明的内容就是：调用类方法时，有几种方式：
- ```Tclass.test(t, 1)```，既类名加方法名，然后传入的参数中```__self___```被赋值为实例```t```。
- ```Tclass.test(Tclass, 1)```, 既类名加方法名，然后传入类本身作为```__self__```。
- ```t.test(1)```，既类实例加方法名，不传入```__self__```。


#### 生成器函数

一个使用```yield```语句的函数或者方法，称为生成器函数。被调用时，总是会返回一个可以执行函数体的**迭代器对象**：调用该迭代器的```__next__()```方法，将会导致这个函数一直运行，直到它的```yield```语句提供了一个值为止。

详情参考 ```yield```章节，这里只提供简单的例子。

```python
>>> def test():
...     i = 0
...     while i<10:
...         yield i
...         i+=1
...
>>> a = test()
>>> a
<generator object test at 0x10e3bb570>
>>> next(a)
0
>>> next(a)
1
>>> a.__next__()
2
>>> a.__next__()
3
>>> a.__next__()
4
>>> a.__next__()
5
>>> a.__next__()
6
>>> a.__next__()
7
>>> a.__next__()
8
>>> a.__next__()
9
>>> a.__next__()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

可以看到```test()```函数返回的是一生成器对象。调用```next(a)```既调用```a.__next__()```，可以返回 ```i```的值。当```test```运行到```i==10```时，生成器也会抛出一个```StopIteration```。

#### 协程函数

使用 ```async def```定义的函数或者方法被称为协程函数。被调用时会返回一个**协程对象**```coroutine```。一个协程函数可能包含```await```表达式，```async with``` 和 ```async for```语句。

详情参考```协程```相关章节，这里只做简单的示例。

```python
async def test1():
    print('test 1')

import asyncio

loop = asyncio.get_event_loop()
task = loop.create_task(test1())
task = loop.create_task(test1())
task = loop.create_task(test1())
loop.run_until_complete(task)

test 1
test 1
test 1
```

#### 异步生成器函数

使用 ```async def```来创建，并包含了```yield```语句的函数或者方法，称为异步生成器函数。该函数在被调用时会返回一个异步迭代器对象，可以在 ```async for```语句中执行函数体。

```python
>>> async def test2():
...     i = 9
...     while True:
...        print(i)
...        yield i
...        i+=1
>>> a=test2()
>>>
>>> a
<async_generator object test2 at 0x10eaa3ae8>
```

#### 内置函数

内置函数对象是对于 C 函数的外部封装。内置函数的例子包括 len() 和 math.sin() (math 是一个标准内置模块)。内置函数参数的数量和类型由 C 函数决定。特殊的只读属性: __doc__ 是函数的文档字符串，如果没有则为 None; __name__ 是函数的名称; __self__ 设定为 None (参见下一条目); __module__ 是函数所属模块的名称，如果没有则为 None。

#### 内置方法

此类型实际上是内置函数的另一种形式，只不过还包含了一个传入 C 函数的对象作为隐式的额外参数。内置方法的一个例子是 alist.append()，其中 alist 为一个列表对象。在此示例中，特殊的只读属性 __self__ 会被设为 alist 所标记的对象。

#### 类

类是可调用的。此种对象通常是作为“工厂”来创建自身的实例，类也可以有重载 __new__() 的变体类型。调用的参数会传给 __new__()，而且通常也会传给 __init__() 来初始化新的实例。

#### 类实例

任意类的实例通过在所属类中定义 __call__() 方法即能成为可调用的对象。

### **注意：以下内容提供引用自官网：[pythondoc](https://docs.python.org/zh-cn/3/reference/datamodel.html),亦可移步官网进行查看**


### NotImplemented

此类型只有一种取值。是一个具有此值的单独对象。此对象通过内置名称 NotImplemented 访问。数值方法和丰富比较方法如未实现指定运算符表示的运算则应返回此值。(解释器会根据指定运算符继续尝试反向运算或其他回退操作)。它的逻辑值为真。

### Ellipsis

此类型只有一种取值。是一个具有此值的单独对象。此对象通过字面值 ... 或内置名称 Ellipsis 访问。它的逻辑值为真。

### numbers.Number, 与此相关的内容可以参考[数字类型](http://www.gopy.wang/archives/Python+1+%E5%86%85%E7%BD%AE%E7%B1%BB%E5%9E%8B+-+%E6%95%B0%E5%AD%97%E7%B1%BB%E5%9E%8B/)

此类对象由数字字面值创建，并会被作为算术运算符和算术内置函数的返回结果。数字对象是不可变的；一旦创建其值就不再改变。Python 中的数字当然非常类似数学中的数字，但也受限于计算机中的数字表示方法。

#### numbers.Integral

此类对象表示数学中整数集合的成员 (包括正数和负数)。

整型数可细分为两种类型:

- 整型 (int)

此类对象表示任意大小的数字，仅受限于可用的内存 (包括虚拟内存)。在变换和掩码运算中会以二进制表示，负数会以 2 的补码表示，看起来像是符号位向左延伸补满空位。

- 布尔型 (bool)
此类对象表示逻辑值 False 和 True。代表 False 和 True 值的两个对象是唯二的布尔对象。布尔类型是整型的子类型，两个布尔值在各种场合的行为分别类似于数值 0 和 1，例外情况只有在转换为字符串时分别返回字符串 "False" 或 "True"。

#### numbers.Real (float)

此类对象表示机器级的双精度浮点数。其所接受的取值范围和溢出处理将受制于底层的机器架构 (以及 C 或 Java 实现)。Python 不支持单精度浮点数；支持后者通常的理由是节省处理器和内存消耗，但这点节省相对于在 Python 中使用对象的开销来说太过微不足道，因此没有理由包含两种浮点数而令该语言变得复杂。

#### numbers.Complex (complex)

此类对象以一对机器级的双精度浮点数来表示复数值。有关浮点数的附带规则对其同样有效。一个复数值 z 的实部和虚部可通过只读属性 z.real 和 z.imag 来获取

### 序列，与此相关内容参考[序列相关](http://www.gopy.wang/archives/Python+1+-+%E5%86%85%E7%BD%AE%E7%B1%BB%E5%9E%8B+-+%E5%BA%8F%E5%88%97%EF%BC%881%EF%BC%89/)

   此类对象表示以非负整数作为索引的有限有序集。内置函数 len() 可返回一个序列的条目数量。当一个序列的长度为 n 时，索引集包含数字 0, 1, ..., n-1。序列 a 的条目 i 可通过 a[i] 选择。

   序列还支持切片: a[i:j] 选择索引号为 k 的所有条目，i <= k < j。当用作表达式时，序列的切片就是一个与序列类型相同的新序列。新序列的索引还是从 0 开始。

   有些序列还支持带有第三个 "step" 形参的 "扩展切片": a[i:j:k] 选择 a 中索引号为 x 的所有条目，x = i + n*k, n >= 0 且 i <= x < j。

#### 不可变序列

不可变序列类型的对象一旦创建就不能再改变。(如果对象包含对其他对象的引用，其中的可变对象就是可以改变的；但是，一个不可变对象所直接引用的对象集是不能改变的。)

以下类型属于不可变对象:

- 字符串

    字符串是由 Unicode 码位值组成的序列。范围在 U+0000 - U+10FFFF 之内的所有码位值都可在字符串中使用。Python 没有 char 类型；而是将字符串中的每个码位表示为一个长度为 1 的字符串对象。内置函数 ord() 可将一个码位由字符串形式转换成一个范围在 0 - 10FFFF 之内的整型数；chr() 可将一个范围在 0 - 10FFFF 之内的整型数转换为长度为 1 的对应字符串对象。str.encode() 可以使用指定的文本编码将 str 转换为 bytes，而 bytes.decode() 则可以实现反向的解码。

- 元组

    一个元组中的条目可以是任意 Python 对象。包含两个或以上条目的元组由逗号分隔的表达式构成。只有一个条目的元组 ('单项元组') 可通过在表达式后加一个逗号来构成 (一个表达式本身不能创建为元组，因为圆括号要用来设置表达式分组)。一个空元组可通过一对内容为空的圆括号创建。

- 字节串

    字节串对象是不可变的数组。其中每个条目都是一个 8 位字节，以取值范围 0 <= x < 256 的整型数表示。字节串字面值 (例如 b'abc') 和内置的 bytes() 构造器可被用来创建字节串对象。字节串对象还可以通过 decode() 方法解码为字符串。

- 可变序列

    可变序列在被创建后仍可被改变。下标和切片标注可被用作赋值和 del (删除) 语句的目标。

#### 可变序列

- 列表

    列表中的条目可以是任意 Python 对象。列表由用方括号括起并由逗号分隔的多个表达式构成。(注意创建长度为 0 或 1 的列表无需使用特殊规则。)

- 字节数组
    
    字节数组对象属于可变数组。可以通过内置的 bytearray() 构造器来创建。除了是可变的 (因而也是不可哈希的)，在其他方面字节数组提供的接口和功能都于不可变的 bytes 对象一致。


### 集合类型

   此类对象表示由不重复且不可变对象组成的无序且有限的集合。因此它们不能通过下标来索引。但是它们可被迭代，也可用内置函数 len() 返回集合中的条目数。集合常见的用处是快速成员检测，去除序列中的重复项，以及进行交、并、差和对称差等数学运算。

   对于集合元素所采用的不可变规则与字典的键相同。注意数字类型遵循正常的数字比较规则: 如果两个数字相等 (例如 1 和 1.0)，则同一集合中只能包含其中一个。

目前有两种内生集合类型:

- 集合
此类对象表示可变集合。它们可通过内置的 set() 构造器创建，并且创建之后可以通过方法进行修改，例如 add()。

- 冻结集合
此类对象表示不可变集合。它们可通过内置的 frozenset() 构造器创建。由于 frozenset 对象不可变且 hashable，它可以被用作另一个集合的元素或是字典的键。


### 映射

此类对象表示由任意索引集合所索引的对象的集合。通过下标 a[k] 可在映射 a 中选择索引为 k 的条目；这可以在表达式中使用，也可作为赋值或 del 语句的目标。内置函数 len() 可返回一个映射中的条目数。

目前只有一种内生映射类型:

- 字典
此类对象表示由几乎任意值作为索引的有限个对象的集合。不可作为键的值类型只有包含列表或字典或其他可变类型，通过值而非对象编号进行比较的值，其原因在于高效的字典实现需要使用键的哈希值以保持一致性。用作键的数字类型遵循正常的数字比较规则: 如果两个数字相等 (例如 1 和 1.0) 则它们均可来用来索引同一个字典条目。

字典是可变的；

![image.png](https://images.xiaozhuanlan.com/photo/2019/e2f991266536762eef483600b1cf0a1c.png)


