# Python - 高级教程 - 数据模型（4） - 元类与多继承

上一章节，我们了解了 `python` 中类的创建和类的基本的属性，本章节我们将主要讲解`元类与多继承`。

# 元类


默认情况下，类是使用 `type()` 来构建的。
元类就是 `Python` 中用来创建类的类。

类体会在一个新的命名空间内执行，类名会被局部绑定到 `type(name, bases, namespace)` 的结果。

类创建过程可通过在定义行传入 `metaclass` 关键字参数，或是通过继承一个包含此参数的现有类来进行定制。

在以下示例中，`MyClass` 和 `MySubclass` 都是 Meta 的实例:


```python
class Meta(type):
    # 继承了 type 作为元类
    pass

class MyClass(metaclass=Meta):
    # 显示指定元类 Meta
    pass

class MySubclass(MyClass):
    # 继承了父类，父类是元类
    pass
```


如之前所说， ```Human``` 是 `type` 类型，而 `Human`又是一个类，所以`type` 其实是一个用来创建类的类，即元类。

那么我们定义 `Human`  的过程，即 `type` 类创建 `type` 类型的实例的过程。

```python
Human1 = type("Human1", (object,), dict(name="", age="", sex=""))
```

通过内置关键字 `type`，通过参数`Human1` 作为类名，`object` 作为继承的父类，`dict()`作为创建类的成员变量，成功的创建了一个类`Human1`。


在类定义内指定的任何其他关键字参数都会在下面所描述的所有元类操作中进行传递。

> 当一个类定义被执行时，将发生以下步骤:
- 解析 MRO 条目；
- 确定适当的元类；
- 准备类命名空间；
- 执行类主体；
- 创建类对象。


![](https://raw.githubusercontent.com/tsbxmw/gopy/master/Pages/Python/images/2/3-2.png)


## 解析 MRO 条目

MRO 即【方法解析顺序】（Method Resolution Order）。

此属性是由类组成的元组，在方法解析期间会基于它来查找基类。

### C3算法

`python` 在发展过程中，也不断的进化了它的 `MRO` 算法，当前是 `C3` 算法。
`C3` 算法保证了即使存在 '钻石形' 继承结构即有多条继承路径连到一个共同祖先也能保持正确的行为。

> C3 算法规则

以 class A(B,C) 为例：

- MRO(object) = [object]
- MRO(A(B, C)) = [A] + merge(MRO(B)， MRO(C), [B, C])

这里的关键在于 merge，其输入是一组列表，按照如下方式输出一个列表：

- 检查第一个列表的头元素（如 L[B] 的头），记作 H。
- 若 H 未出现在其它列表的尾部，则将其输出，并将其从所有列表中删除
- 否则，取出下一个列表的头部记作 H，继续该步骤
- 重复上述步骤:
- 如果是列表为空，则算法结束；
- 如果是不能再找出可以输出的元素，说明无法构建继承关系，Python 会抛出异常。



> 下面通过一个例子讲解 `C3` 算法查找继承父类的顺序列表是如何生成的。


![](https://raw.githubusercontent.com/tsbxmw/gopy/master/Pages/Python/images/2/3-1.png)


```python
class A(object):
    pass

class B(object):
    pass

class C(A, B):
    pass

class D(A):
    pass

class E(D, C):
    pass

print(A.mro())
print(B.mro())
print(C.mro())
print(D.mro())
print(E.mro())
```


> 这里我们先不公布结果，先利用 `C3` 算法解析以下，是否与输出相同？


```python
- MRO(A) = [A] + merge(MRO(object))
         = [A, object]

- MRO(B) = [B] + merge(MRO(object))
         = [B, object]

- MRO(D(A)) = [D] + merge(MRO(A), [A])
            = [D] + merge([A, object], [A])
            # 此处 遍历 A，A出现在 [A] 中且是第一个，删除 A，并入 [D]
            = [D, A] + merge([object], [])
            # 此处 遍历 object， object 没有出现在其他列表中， 删除 object，并入[D, A]
            = [D, A, object] + merge([], [])
            # 列表为空
            = [D, A, object]
- MRO(C(A,B)) = [C] + merge(MRO(A), MRO(B), [A, B])
              = [C] + merge([A, object], [B, object], [A, B])
              # 此处 遍历 A， A 出现在 [A, B] 中且是第一个值，则 删除 A, 并入 [C]
              = [C, A] + merge([object], [B, object], [B])
              # 此处 遍历 object， object出现在 [B,object] 中，但不是第一个，继续遍历
              # 此处 遍历 B, B 出现在 [B] 中，且是第一个值， 则 删除 B, 并入 [C, A]
              = [C, A, B] + merge([object], [object], [])
              # 此处遍历 object， object 出现在第二个列表中，则删除 object, 并入 [C, A, B]
              = [C, A, B, object] + merge([], [], [])
              # 列表 为空
              = [C, A, B, object]
- MRO(E(D, C)) = [E] + merge(MRO(D), MRO(C), [D, C])
               = [E] + merge([D, A, object], [C, A, B, object], [D, C])
               # 此处遍历 D， D出现在 [D,C ] 中，且是第一个，删除 D，并入 [E]
               = [E, D] + merge([A, object], [C, A, B, object], [C])
               # 此处 遍历 A , A 出现在 [C, A, B, object] 中，但不是第一个，继续遍历
               # 此处 遍历 object， object出现在 [C, A, B, object] 中，但不是第一个，继续遍历
               # 此处 遍历 C，C 出现在 [c] 中且是第一个，删除 C, 并入 [E, D]
               = [E, D, C] + merge([A, object], [A, B, object], [])
               # 此处 遍历 A，A出现在 [A, B, object ] 中，且是第一个，删除 A， 并入 [E, D, C]
               = [E, D, C, A] + merge([object], [B, object], [])
               # 此处 遍历 object， object出现在 [B, object] 中，但不是第一个，继续遍历
               # 此处 遍历 B， B 没有出现在 其他列表中，删除 B，并入 [E, D, C, A]
               = [E, D, C, A, B] + merge([object], [object], [])
               = [E, D, C, A, B, object] + merge([], [], [])
               = [E, D, C, A, B, object]
```

最后的值为 ：

```shell
A = [A, object]
B = [B, object]
C = [C, A, B, object]
D = [D, A, object]
E = [E, D, C, A, B, object]
```

执行输出结果如下：

```shell
[<class '__main__.A'>, <class 'object'>]
[<class '__main__.B'>, <class 'object'>]
[<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class 'object'>]
[<class '__main__.D'>, <class '__main__.A'>, <class 'object'>]
[<class '__main__.E'>, <class '__main__.D'>, <class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class 'object'>]
```

输出的值与推算的结果相同。


## 确定适当的元类

为一个类定义确定适当的元类是根据以下规则:

- 如果没有基类且没有显式指定元类，则使用 type()；
- 如果给出一个显式元类而且 不是 type() 的实例，则其会被直接用作元类；
- 如果给出一个 type() 的实例作为显式元类，或是定义了基类，则使用最近派生的元类。

最近派生的元类会从显式指定的元类（如果有）以及所有指定的基类的元类（即 type(cls)）中选取。
最近派生的元类应为 所有 这些候选元类的一个子类型。
如果没有一个候选元类符合该条件，则类定义将失败并抛出 TypeError。

## 准备类命名空间

一旦适当的元类被确定，则类命名空间将会准备好。如果元类具有 `__prepare__` 属性，它会以 `namespace = metaclass.__prepare__(name, bases, **kwds)` 的形式被调用（其中如果有附加的关键字参数，应来自类定义）。

如果元类没有 `__prepare__` 属性，则类命名空间将初始化为一个空的有序映射。

### 这里我们来说一下命名空间 [`namespace`]

namespace （命名空间）是一个从名字到对象的映射。 

大部分命名空间当前都由 Python 字典实现，但一般情况下基本不会去关注它们（除了要面对性能问题时），而且也有可能在将来更改。

> 下面是几个命名空间的例子：
- 存放内置函数的集合（包含 abs() 这样的函数，和内建的异常等）；
- 模块中的全局名称；函数调用中的局部名称。 
- 从某种意义上说，对象的属性集合也是一种命名空间的形式。 

关于命名空间的重要一点是，不同命名空间中的名称之间绝对没有关系！关于这点，通过以下例子可以了解

```python
class A:
    a = 1
class B:
    b = 2

A.a 
B.a
```

尽管 A、B 处于同一命名空间，但是他们还包含自己的命名空间，而自己的命名空间中的属性名称之前是毫无关联的。

> 在不同时刻创建的命名空间拥有不同的生存期
- 包含内置名称的命名空间是在 Python 解释器启动时创建的，永远不会被删除。
- 模块的全局命名空间在模块定义被读入时创建；通常，模块命名空间也会持续到解释器退出。
- 被解释器的顶层调用执行的语句，从一个脚本文件读取或交互式地读取，被认为是 __main__ 模块调用的一部分，因此它们拥有自己的全局命名空间。（内置名称实际上也存在于一个模块中；这个模块称作 builtins 。）
- 一个函数的本地命名空间在这个函数被调用时创建，并在函数返回或抛出一个不在函数内部处理的错误时被删除。（事实上，比起描述到底发生了什么，忘掉它更好。）当然，每次递归调用都会有它自己的本地命名空间。
- 一个 作用域 是一个命名空间可直接访问的 Python 程序的文本区域。 这里的 “可直接访问” 意味着对名称的非限定引用会尝试在命名空间中查找名称。


 而 命名空间的搜索规则如下：
- 最先搜索的最内部作用域包含局部名称
- 从最近的封闭作用域开始搜索的任何封闭函数的范围包含非局部名称，也包括非全局名称
- 倒数第二个作用域包含当前模块的全局名称
- 最外面的范围（最后搜索）是包含内置名称的命名空间

> 关于全局变量：
- 如果一个名称被声明为全局变量，则所有引用和赋值将直接指向包含该模块的全局名称的中间作用域。
- 要重新绑定在最内层作用域以外找到的变量，可以使用 nonlocal 语句声明为非本地变量。 
- 如果没有被声明为非本地变量，这些变量将是只读的（尝试写入这样的变量只会在最内层作用域中创建一个 新的 局部变量，而同名的外部变量保持不变）。

通常，当前局部作用域将（按字面文本）引用当前函数的局部名称。 在函数以外，局部作用域将引用与全局作用域相一致的命名空间：模块的命名空间。 类定义将在局部命名空间内再放置另一个命名空间。

重要的是应该意识到作用域是按字面文本来确定的：在一个模块内定义的函数的全局作用域就是该模块的命名空间，无论该函数从什么地方或以什么别名被调用。 另一方面，实际的名称搜索是在运行时动态完成的 --- 但是，语言定义在 编译时 是朝着静态名称解析的方向演化的，因此不要过于依赖动态名称解析！ （事实上，局部变量已经是被静态确定了。）

Python 的一个特殊之处在于 -- 如果不存在生效的 global 语句 -- 对名称的赋值总是进入最内层作用域。 赋值不会复制数据 --- 它们只是将名称绑定到对象。 删除也是如此：语句 `del x` 会从局部命名空间的引用中移除对 `x` 的绑定。

 事实上，所有引入新名称的操作都使用局部作用域：
- `import` 语句和函数定义会在局部作用域中绑定模块或函数名称。
- `global` 语句可被用来表明特定变量生存于全局作用域并且应当在其中被重新绑定；
- `nonlocal` 语句表明特定变量生存于外层作用域中并且应当在其中被重新绑定。


## 执行类主体

类主体会以（类似于）` exec(body, globals(), namespace)` 的形式被执行。普通调用与 `exec()` 的关键区别在于当类定义发生于函数内部时，词法作用域允许类主体（包括任何方法）引用来自当前和外部作用域的名称。

但是，即使当类定义发生于函数内部时，在类内部定义的方法仍然无法看到在类作用域层次上定义的名称。类变量必须通过实例的第一个形参或类方法来访问，或者是通过下一节中描述的隐式词法作用域的 `__class__` 引用。

## 创建类对象

一旦执行类主体完成填充类命名空间，将通过调用 `metaclass(name, bases, namespace, **kwds)` 创建类对象（此处的附加关键字参数与传入 `__prepare__` 的相同）。

如果类主体中有任何方法引用了 `__class__` 或 `super`，这个类对象会通过零参数形式的 `super(). __class__` 所引用，这是由编译器所创建的隐式闭包引用。这使用零参数形式的 super() 能够正确标识正在基于词法作用域来定义的类，而被用于进行当前调用的类或实例则是基于传递给方法的第一个参数来标识的。

> 在 CPython 3.6 及之后的版本中，`__class__` 单元会作为类命名空间中的条目被传给元类。 如果存在，它必须被向上传播给` type.__new__ `调用，以便能正确地初始化该类

当使用默认的元类 `type` 或者任何最终会调用 `type.__new__` 的元类时，以下额外的自定义步骤将在创建类对象之后被发起调用:

- 首先，`type.__new__` 将收集类命名空间中所有定义了 `__set_name__()` 方法的描述器；
- 接下来，所有这些 `__set_name__` 方法将使用所定义的类和特定描述器所赋的名称进行调用；
- 最后，将在新类根据方法解析顺序所确定的直接父类上调用 __init_subclass__() 钩子。

在类对象创建之后，它会被传给包含在类定义中的类装饰器（如果有的话），得到的对象将作为已定义的类绑定到局部命名空间。

当通过 `type.__new__` 创建一个新类时，提供以作为命名空间形参的对象会被复制到一个新的有序映射并丢弃原对象。这个新副本包装于一个只读代理中，后者则成为类对象的 `__dict__` 属性。


## 实例

下面，我们根据上面的元类的内容，写出了下面这个例子。

```python
class TestMeta(type):
    def __new__(cls, name, bases, attrs):
        print("i am in test meta __new__")
        print(name, bases, attrs)
        attrs["a"] = 1
        return type.__new__(cls, "A", (object,), dict(A.__dict__))

    @classmethod
    def __prepare__(mcs, name, bases):
        print("i am in test meta __prepare__")
        print(name, bases)
        return {}


class A(object):
    def __init__(self):
        print("i am in A __init__")
        self.a = 1


class B(metaclass=TestMeta):
    b = 1

    def __new__(cls):
        print("i am in B __new__")
        return super().__new__(cls)


if __name__ == "__main__":
    b = B()
    print(b.a)
    print(type(b))
    print(B.__dict__)
    print(A.__dict__)
    a = A()
    print(a.a)
    print(type(a))

    print(type(A))
    print(type(B))

```

```shell
i am in test meta __prepare__
B ()
i am in test meta __new__
B () {'__module__': '__main__', '__qualname__': 'B', 'b': 1, '__new__': <function B.__new__ at 0x1032231e0>, '__classcell__': <cell at 0x1031efa98: empty>}
Python/Python2/3-1.py:21: DeprecationWarning: __class__ not set defining 'B' as <class '__main__.A'>. Was __classcell__ propagated to type.__new__?
  class B(metaclass=TestMeta):
i am in A __init__
1
<class '__main__.A'>
{'__module__': '__main__', '__init__': <function A.__init__ at 0x103223158>, '__dict__': <attribute '__dict__' of 'A' objects>, '__weakref__': <attribute '__weakref__' of 'A' objects>, '__doc__': None}
{'__module__': '__main__', '__init__': <function A.__init__ at 0x103223158>, '__dict__': <attribute '__dict__' of 'A' objects>, '__weakref__': <attribute '__weakref__' of 'A' objects>, '__doc__': None}
i am in A __init__
1
<class '__main__.A'>
```

我们发现， `b` 的 `type` 竟然是 `<class '__main__.A'>`。也就是说，通过元类的指定，我们定制化了 `B` 类的实例的创建过程，偷梁换柱，将`B()` 返回了 `A` 的实例 `a`。

具体的实现就是:
```python
        return type.__new__(cls, "A", (object,), dict(A.__dict__))
```

我们来分析一下 `B()` 的过程：

- 解析 MRO 条目，继承了` (<class '__main__.B'>, <class 'object'>)`
- 确定适当的元类：这里显示声明了为 `TestMeta`
- 准备类命名空间：`__prepare__`
- 执行类主体：exec
- 创建类对象：`TestMeta.__new__` ==> `A`
- 创建类实例：`type.__new__`

最后返回了 `b = B()` 已经在 创建类对象的时候替换为 `A` 了。

# 类的初始化

了解了类的创建是由 `type` 元类控制的，那么我们来看下自定义类在除去自定义元类的控制后是如何初始化一个对象的呢？

我们依旧沿用上面的例子，StrSub。

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

```python
__new__ begin
<class '__main__.StrSub'>
test
__new__ over
__init__ begin
test
__init__ over
```

通过上面对 `__new__` 和 `__init__` 的了解，我们可以了解到类初始化的顺序。
关于`__new__` 和 `__init__` 的方法的说明，不了解的可以阅读上一章的内容。

![](https://images.xiaozhuanlan.com/photo/2019/af181d615a7a7d88a2bc9e8e6db20902.png)

所以说， `__new__` 是用来创建类实例的，而 `__init__` 是用来定制化 类实例的。

我们注意到 `__new__` 中使用了 `super().__new__` 方法来利用父类产生子对象。

```python
super().__new__(cls, test)
```

### super() 和 多继承

提到类的继承，就离不开多继承，就离不开父类。

其实单继承比较好理解，这里就不在赘述，我们来看下一个多继承的问题。

#### 多继承

对于多数应用来说，在最简单的情况下，你可以认为搜索从父类所继承属性的操作是深度优先、从左至右的，当层次结构中存在重叠时不会在同一个类中搜索两次。 

先来看一个简单地多继承：

![](https://images.xiaozhuanlan.com/photo/2019/d3103474aee362d3e2eb02e0dee9c3f9.png)

```python
class A(object):
    def __init__(self, a):
        print("A __init__ begin")
        self.a = a
        print("A __init__ end")

    def test(self):
        print("A test begin")
        print(self.a)
        print("A test end")


class B(object):
    def __init__(self, b):
        print("B __init__ begin")
        self.b = b
        print("B __init__ end")

    def test(self):
        print("B test begin")
        print(self.b)
        print("B test end")


class C(A, B):
    def __init__(self, a):
        print("C __init__ begin")
        A.a = a
        B.b = a
        super(C, self).__init__(a)
        print("C __init__ end")

    def __new__(cls, a):
        print("C __new__ begin")
        print(a)
        print("C __new__ end")
        return super().__new__(cls)

    def test(self):
        print("C test begin")
        print(self.a)
        print("C test end")


if __name__ == "__main__":
    c = C("c")
    d = C.mro()
    print(d)
    c.test()
```

```shell
C __new__ begin
c
C __new__ end
C __init__ begin
A __init__ begin
A __init__ end
C __init__ end
[<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class 'object'>]
C test begin
c
C test end
```


尽管 类 `C` 继承了 `A,B` 两个类，但是执行 `__init__` 的确只有 `A` ，这里其实就对应上了之前所说的 `__mro__` 搜索顺序。

可以计算出 `C` 的 `MRO`:
```shell
MRO(C(A,B)) = [C, A, B, object]
```

因此，首先回到会到 `A` 中搜索 `__init__`，然后（递归地）到 `A` 的基类中搜索，如果在那里未找到，再到 `B` 中搜索，依此类推。

所以我们改变一下上面的列子：删除掉 `A` 的 `__init__` 方法。

```python
class A(object):
    # def __init__(self, a):
    #     print("A __init__ begin")
    #     self.a = a
    #     print("A __init__ end")

    def test(self):
        print("A test begin")
        print(self.a)
        print("A test end")


class B(object):
    def __init__(self, b):
        print("B __init__ begin")
        self.b = b
        print("B __init__ end")

    def test(self):
        print("B test begin")
        print(self.b)
        print("B test end")


class C(A, B):
    def __init__(self, a):
        print("C __init__ begin")
        A.a = a
        B.b = a
        super(C, self).__init__(a)
        print("C __init__ end")

    def __new__(cls, a):
        print("C __new__ begin")
        print(a)
        print("C __new__ end")
        return super().__new__(cls)

    def test(self):
        print("C test begin")
        print(self.a)
        print("C test end")

if __name__ == "__main__":
    c = C("c")
    d = C.mro()
    print(d)
    c.test()
```

```shell
C __new__ begin
c
C __new__ end
C __init__ begin
B __init__ begin
B __init__ end
C __init__ end
[<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class 'object'>]
C test begin
c
C test end
```

果然，当 第一顺位 `A` 没有找到方法是， `super().__init__()` 搜索到了 `B.__init__()`，并执行了它。

真实情况比这个更复杂一些；方法解析顺序会动态改变以支持对 super() 的协同调用。 这种方式在某些其他多重继承型语言中被称为后续方法调用，它比单继承型语言中的 super 调用更强大。

动态改变顺序是有必要的，因为所有多重继承的情况都会显示出一个或更多的菱形关联（即至少有一个父类可通过多条路径被最底层类所访问）。


### 使用 `__new__` 的实例

我们需要定制一个类 `UpperStr`, 用来存储字符串，但是会将字符串自动转为大写的。

根据我们上面了解的 类 的常见过程，我们可以写出如下代码。

```python
class UpperStr(str):
    def __init__(self, string):
        print("__init__ begin")
        self.test = string
        print(self.test)
        print("__init__ over")

    def __new__(cls, string):
        print("__new__ begin")
        print(cls)
        print(string)
        print("__new__ over")
        string = string.upper()
        return super(UpperStr, cls).__new__(cls, string)


if __name__ == "__main__":
    ss = UpperStr("test")
    print(ss)
```

我们只需要在创建 str 对象之前，讲传入 str 的值使用 `upper()` 函数变为全大写拼写即可。

> 关于元类与类初始化的内容就先到这里，有兴趣的可以查看官方文档：

- https://docs.python.org/zh-cn/3/tutorial/classes.html
- https://docs.python.org/zh-cn/3/reference/datamodel.html