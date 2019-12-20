# Python - 高级教程 - 数据模型（3）

在上一章节中，我们了解了模块 `module` 的导入和使用。
本章将主要说明 类 相关内容，关于 类，大家都不陌生，尤其是在 `python` 中，`万物皆类`。

> 下一章节，将主要讲解类的初始化过程和类的多继承问题。

#  python 中的 类

![](https://images.xiaozhuanlan.com/photo/2019/9ff89e6fb7b3273a6122579dca1bc079.png)

在 `python` 中，整数`int`的实现方式如上所示。这里的 `1` 并不只是字面上的 `1`，其实它也是 `<class 'int'>` 的实例，如果使用 `dir(1)` 来查看的话，可以更明显的看出它的属性。

```python
>>> dir(1)
['__abs__', '__add__', '__and__', '__bool__', '__ceil__', '__class__', '__delattr__', '__dir__', '__divmod__', '__doc__', '__eq__', '__float__', '__floor__', '__floordiv__', '__format__', '__ge__', '__getattribute__', '__getnewargs__', '__gt__', '__hash__', '__index__', '__init__', '__init_subclass__', '__int__', '__invert__', '__le__', '__lshift__', '__lt__', '__mod__', '__mul__', '__ne__', '__neg__', '__new__', '__or__', '__pos__', '__pow__', '__radd__', '__rand__', '__rdivmod__', '__reduce__', '__reduce_ex__', '__repr__', '__rfloordiv__', '__rlshift__', '__rmod__', '__rmul__', '__ror__', '__round__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__', '__rtruediv__', '__rxor__', '__setattr__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', '__truediv__', '__trunc__', '__xor__', 'bit_length', 'conjugate', 'denominator', 'from_bytes', 'imag', 'numerator', 'real', 'to_bytes']
```

我们知道，`type()` 内置方法，可以用来查看`python`中实例的类型。

```python
>>> a = 1
>>> b = type(a)
>>> b
<class 'int'>
>>> c = type(b)
>>> c
<class 'type'>
>>> d = type(c)
>>> d
<class 'type'>
```

可以很清晰的看到:

整数类型 a 的类型为 b : ```<class 'int'>```
而 b 的类型 c: ```<class 'type'>```
但是从 c:```class 'type'>```开始，无论我们再如何的去查询 c 的类型，也只能查找到 ```type``` 类。

```python

>>> object
<class 'object'>
>>> type(object)
<class 'type'>
```

在`python` 中，```<class type>```作为所有对象的父类而存在，当我们创建类时，所默认继承的`object`，也是一个类```<class 'object'>```，而它也是`<class 'type'>`类型。

那么我们创建自定义类或者使用系统内置类的时候，它又是如何工作的呢。

## 类的创建

### 首先让我们来看一个很简单的例子。在 `python` 中，创建一个类需要使用关键字 `class`。

```python
class Human(object):
    name = ""
    sex = ""
    age = ""
```

这是我们创建的 ```Human``` 类，它继承自```object```，包含了3个属性，`name,sex,age` 即 姓名/性别/年龄。

Note： 就算我们不显示的继承 object 父类，`python` 也会默认继承。

```python
>>> class Human(object):
...     name = ""
...     sex = ""
...     age = ""
... 
>>> type(Human)
<type 'type'>
>>> Human
<class '__main__.Human'>
```

### 使用自定义类`Human1`区创建一个实例`human1`。

```python
>>> Human1 = type("Human1", (object,), dict(name="", age="", sex=""))
>>> human1 = Human1()
>>> human1
<__main__.Human1 object at 0x10eecb550>
>>> type(human1)
<class '__main__.Human1'>
>>> type(Human1)
<class 'type'>
```
`Human1` 与 `Human` 在使用上来说并无区别。


## 类的属性

要想了解类，我们需要先了解一下类的关键属性。
使用 `dir()` 查看类的属性。

```python
>>> dir(a)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'age']
```

#### __class__

类的类型，这里我使用 `type(a)==a.__class__`，结果为 `True`，说明 `type` 取得值也为 `__class__`。这里可以使用这个类型区创建与 `a` 类型相同的对象。

```python
>>> a.__class__
<class '__main__.Human'>
>>> type(a.__class__)
<class 'type'>
>>> type(a)==a.__class__
True
```

#### __delattr__

实现了此方法的类，当 `del()` 方法调用时，实际上是调用的此方法。详细看下面的例子。

```python
>>> a.__delattr__
<method-wrapper '__delattr__' of Human object at 0x1032b5240>
>>> a.__delattr__()  # 这里说明 需要一个参数
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: expected 1 arguments, got 0
>>> a.age
11
>>> del(a.age)  # 使用  del()
>>> a.age
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Human' object has no attribute 'age'
>>> a.age = 11
>>> a.__delattr__("age")  # 使用 __delattr__ 与 del() 的效果相同。
>>> a.age
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Human' object has no attribute 'age'
```

#### __dict__

存储了当前类的成员变量。

```python
>>> a.__dict__
{}
>>> a.age = 1
>>> a.__dict__
{'age': 1}
```

#### __dir__

实现了此方法后，使用内置函数`dir()`时，返回的为此方法。

```python
>>> b = a.__dir__()
>>> b.sort()
>>> b
['__age__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
>>> c = dir(a)
>>> c.sort()
>>> c
['__age__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
>>>
```

#### __doc__

该对象的文档字符串，没有则为 `None`；不会被子类继承。

```python
>>> a.__doc__
>>> type(a.__doc__)
<class 'NoneType'>
```

#### __eq__(self, other); __le__, __lt__, __ne__, __gt__, __ge__


以上这些被称为“富比较”方法。运算符号与方法名称的对应关系如下：
-  x<y 调用 x.__lt__(y);
- x<=y 调用 x.__le__(y)
- x==y 调用 x.__eq__(y)
- x!=y 调用 x.__ne__(y)
- x>y 调用 x.__gt__(y)
- x>=y 调用 x.__ge__(y)。

如果指定的参数对没有相应的实现，富比较方法可能会返回单例对象 `NotImplemented`。

按照惯例，成功的比较会返回 `False` 或 `True`。不过实际上这些方法可以返回任意值，因此如果比较运算符是要用于布尔值判断（例如作为 if 语句的条件），`Python` 会对返回值调用 `bool()` 以确定结果为真还是假。

```python
>>> a.__eq__
<method-wrapper '__eq__' of Human object at 0x1032b5240>
>>> a.__eq__(1)
NotImplemented
>>> a.__eq__(a)
True
```

由于我们没有显示的实现 `Human` 与 `int` 的比较，所以会有 `NotImplemented` 的提示。

#### __format__(self, format_spec)

通过 `format()` 内置函数、扩展、格式化字符串字面值 的求值以及 `str.format()` 方法调用以生成一个对象的“格式化”字符串表示。 `format_spec` 参数为包含所需格式选项描述的字符串。 `format_spec` 参数的解读是由实现 `__format__() `的类型决定的，不过大多数类或是将格式化委托给某个内置类型，或是使用相似的格式化选项语法。

#### __getattr__(self, name)

获取名称为 `name` 的属性的值。当使用 `getattr(object, name)` 获取 `object` 的 `name` 的属性的值时，将会在调用 `__getattribute__` 发生 `AttributeError `时才会调用此方法。

```python
>>> getattr(a, 'age')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Human' object has no attribute 'age'
>>> a.age = 11
>>> getattr(a, 'age')
11
```

当默认属性访问因引发 `AttributeError` 而失败时被调用 (可能是调用` __getattribute__() `时由于 `name` 不是一个实例属性或 `self` 的类关系树中的属性而引发了 `AttributeError`；或者是对 `name `特性属性调用 `__get__()` 时引发了 `AttributeError`。此方法应当返回（找到的）属性值或是引发一个 `AttributeError` 异常。

> 请注意如果属性是通过正常机制找到的，`__getattr__()` 就不会被调用。
（这是在 `__getattr__()` 和 `__setattr__()` 之间故意设置的不对称性。）
这既是出于效率理由也是因为不这样设置的话 `__getattr__()` 将无法访问实例的其他属性。
要注意至少对于实例变量来说，你不必在实例属性字典中插入任何值（而是通过插入到其他对象）就可以模拟对它的完全控制

#### __setattr__(self, name, value)

此方法在一个属性被尝试赋值时被调用。这个调用会取代正常机制（即将值保存到实例字典）。 `name` 为属性名称， `value` 为要赋给属性的值。

```python
>>> getattr(a, 'test')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Human' object has no attribute 'test'
>>> setattr(a, 'test', 'test111')
>>> getattr(a, 'test')
'test111'
```
如果 `__setattr__()` 想要赋值给一个实例属性，它应该调用同名的基类方法，例如 `object.__setattr__(self, name, value)`。

#### __getattribute__(self, name)

此方法会无条件地被调用以实现对类实例属性的访问。优先级上来说，`__getattribute__ > __getattr__`。

如果类还定义了` __getattr__()`，则后者不会被调用，除非 `__getattribute__()` 显式地调用它或是引发了 `AttributeError`。
如果找到了的话，应当返回属性值，否则引发一个 `AttributeError` 异常。
而为了避免此方法中的无限递归，它的实现应该总是调用具有相同名称的基类方法来访问它所需要的任何属性，例如 `object.__getattribute__(self, name)`。


```python
>>> a.__getattribute__('test')
'test111'
```

#### __hash__

通过内置函数 `hash()` 调用以对哈希集的成员进行操作，属于哈希集的类型包括 `set`、`frozenset` 以及 `dict`。

`__hash__()` 应该返回一个整数。对象比较结果相同所需的唯一特征属性是其具有相同的哈希值；

建议的做法是把参与比较的对象全部组件的哈希值混在一起，即将它们打包为一个元组并对该元组做哈希运算

```python
class Human(object):
      def __hash__(self):
        return hash(self.age, self,name, self.sex)
```

> `hash()` 会从一个对象自定义的 `__hash__()` 方法返回值中截断为 `Py_ssize_t` 的大小。通常对 64 位构建为 8 字节，对 32 位构建为 4 字节。如果一个对象的`__hash__() `必须在不同位大小的构建上进行互操作，请确保检查全部所支持构建的宽度。做到这一点的简单方法是使用 `python -c "import sys; print(sys.hash_info.width)"`。

> 在默认情况下，str 和 bytes 对象的 __hash__() 值会使用一个不可预知的随机值“加盐”。 虽然它们在一个单独 Python 进程中会保持不变，但它们的值在重复运行的 Python 间是不可预测的。
这种做法是为了防止以下形式的拒绝服务攻击：通过仔细选择输入来利用字典插入操作在最坏情况下的执行效率即 O(n^2) 复杂度。详情见 http://www.ocert.org/advisories/ocert-2011-003.html
改变哈希值会影响集合的迭代次序。Python 也从不保证这个次序不会被改变（通常它在 32 位和 64 位构建上是不一致的）。

#### __repr__(self)

由 `repr()` 内置函数调用以输出一个对象的“官方”字符串表示。如果可能，这应类似一个有效的 `Python` 表达式，能被用来重建具有相同取值的对象（只要有适当的环境）。如果这不可能，则应返回形式如 `<...some useful description...>` 的字符串。返回值必须是一个字符串对象。如果一个类定义了` __repr__() `但未定义 `__str__()`，则在需要该类的实例的“非正式”字符串表示时也会使用` __repr__()`。

#### __str__(self)

通过 `str(object)` 以及内置函数 `format()`和 `print()` 调用以生成一个对象的“非正式”或格式良好的字符串表示。返回值必须为一个 字符串 对象。

此方法与 `object.__repr__()` 的不同点在于 `__str__()` 并不预期返回一个有效的 `Python` 表达式：可以使用更方便或更准确的描述信息。

内置类型 `object` 所定义的默认实现会调用 `object.__repr__()`。

```python
>>> print(a)
<__main__.Human object at 0x1032b5240>
>>> str(a)
'<__main__.Human object at 0x1032b5240>'
```

#### __bytes__(self)
通过 bytes 调用以生成一个对象的字节串表示。这应该返回一个 bytes 对象。


#### __new__(cls[,...])

调用以创建一个 cls 类的新实例。

`__new__()` 是一个静态方法 (因为是特例所以你不需要显式地声明)，它会将所请求实例所属的类作为第一个参数。其余的参数会被传递给对象构造器表达式 (对类的调用)。`__new__()` 的返回值应为新对象实例 (通常是 cls 的实例)。

典型的实现会附带适宜的参数使用 `super().__new__(cls[, ...])`，通过超类的 `__new__() `方法来创建一个类的新实例，然后根据需要修改新创建的实例再将其返回。

如果 `__new__()` 在构造对象期间被发起调用并且它返回了一个实例或 `cls` 的子类，则新实例的 `__init__()` 方法将以 `__init__(self[, ...])` 的形式被发起调用，其中 `self` 为新实例而其余的参数与被传给对象构造器的参数相同。

如果 `__new__()` 未返回一个 `cls` 的实例，则新实例的 `__init__()` 方法就不会被执行。

> `__new__()` 的目的主要是允许不可变类型的子类 (例如 `int, str 或 tuple`) 定制实例创建过程。它也常会在自定义元类中被重载以便定制类创建过程。

```python
class StrSub(str):
    def __new__(cls, test):
        print("__new__ begin")
        print(cls)
        print(test)
        print("__new__ over")
        return super().__new__(cls, test)


if __name__ == "__main__":
    ss = StrSub("test")
```

```shell
__new__ begin
<class '__main__.StrSub'>
test
__new__ over
```


#### __init__(self[, ...])

在实例 (通过 `__new__()`) 被创建之后，返回调用者之前调用。其参数与传递给类构造器表达式的参数相同。一个基类如果有 `__init__()` 方法，则其所派生的类如果也有 `__init__()` 方法，就必须$显式$地调用它以确保实例基类部分的正确初始化；例如: `super().__init__([args...])`.

> 因为对象是由 `__new__()` 和 `__init__()` 协作构造完成的 (由 `__new__()` 创建，并由 `__init__()` 定制)，所以 `__init__()` 返回的值只能是 `None`，否则会在运行时引发 `TypeError`。

```python
class StrSub(str):
    def __init__(self, test):
        print("__init__ begin")
        self.test = test
        print(self.test)
        print("__init__ over")

    def __new__(cls, test):
        print("__new__ begin")
        print(cls)
        print(test)
        print("__new__ over")
        return super().__new__(cls, test)

if __name__ == "__main__":
    ss = StrSub("test")
```

```shell
__new__ begin
<class '__main__.StrSub'>
test
__new__ over
__init__ begin
test
__init__ over
```

#### __del__(self)

在实例将被销毁时调用。

如果一个基类具有 `__del__()` 方法，则其所派生的类如果也有 `__del__()` 方法，就必须$显式$地调用它以确保实例基类部分的正确清除。

> 对象重生
`__del__() `方法可以 (但不推荐!) 通过创建一个该实例的新引用来推迟其销毁。这被称为$对象 重生$。
`__del__()` 是否会在重生的对象将被销毁时再次被调用是由具体实现决定的 ；
当前的 `CPython` 实现只会调用一次。

当解释器退出时不会确保为仍然存在的对象调用 `__del__()` 方法。

`del x` 并不直接调用 `x.__del__()`:
-  `del x` 会将 x 的引用计数减 1
-  `x.__del__()` 仅会在 x 的引用计数变为零时被调用。

#### __slots__

`__slots__` 允许我们显式地声明数据成员（例如特征属性）并禁止创建 `__dict__` 和 `__weakref__` (除非是在 __slots__ 中显式地声明或是在父类中可用。)

相比使用 `__dict__` 此方式可以显著地节省空间。 属性查找速度也可得到显著的提升。

例子：

```python
>>> class Human(object):
...     __slots__ = ["age"]
...
>>> a = Human()
>>> a.age
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: age
>>> a.age = 1
>>> a.age
1
>>> a.test = 2
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Human' object has no attribute 'test'
```

当我们定义了 `__slots__` 后，我们就无法向这个 类 中添加不存在这个 `__slots__ `中的属性了。

例如上面，我们将 `__slots__ = ["age"]` 加入到`Human` 中后，当我们添加 `age` 属性时，是可以添加成功的；但是当添加 `test=2` 的属性时，`__slots__` 则阻止了我们继续添加属性，并抛出了 `AttributeError` 。

## 类的初始化和继承

属性相关的内容，先说到这里，下一章我们重点讨论类的初始化和继承先关的问题。

大家也可以配合官方文档食用，效果更佳。
https://docs.python.org/zh-cn/3/reference/datamodel.html#objects-values-and-types
