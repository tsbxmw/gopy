# Python  - 高级用法 - 数据模型（2）

很多人在写代码的时候不考虑代码的底层运行逻辑，导致出现问题后，不明白问题出在哪里，哪怕通过搜索解决了问题，当再次遇到这个问题的时候，往往还是会陷入困境。

所以，了解并掌握代码的实际运行规则后再去编码，比只了解语法后就直接书写往往会避免某些陷阱。

在学习一门语言的语法书写规范后，深入了解整个语言的基础设计、编译、运行过程，往往有助于我们对这门语言的掌握，提升自己的工作效率，写出更高质量的代码。

> 本章节内容，只对 ```module``` 和 ```python``` 的模块导入系统进行了详细讲解。

## 模块

模块，是```python```代码的基本组织单元，由```导入系统```创建，由```import```语句发起调用。
下面我们分别来解释一下这句话中的名词。

### module

 ```module```对象也是```python```代码的一种组织单位。各个模块具有独立的命名空间，可包含任意的```python```对象。

```python
>>> import os
>>> os
<module 'os' from '/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/os.py'>
```

对 ```python```来说， ```module```也是对象。

```python
>>> type(os)
<class 'module'>
>>> type(type(os))
<class 'type'>
```

而 ```module```是如何被创建和导入到系统中的呢？


### 导入系统

 ```python``` 的 ```导入系统```是用来访问```module```内代码的一套逻辑。

> 发起调用```导入机制```的常用方式：```import```语句。
也可以通过 ```importlib.import_module()```以及内置的```__import__()```函数来发起调用。

```python
>>> import os
>>> type(os)
<class 'module'>
```

### ```import```语句结合了两个操作：

> 1， 搜索指定名称的模块，将搜索结果绑定到当前作用域的名称。```import```语句的搜索操作定义为对```__import__()```函数的带参数的调用。

- 为了开始搜索，Python 需要被导入模块的完整限定名称。此名称可以来自```import```语句所带的各种参数，也可以来自传给```importlib.import_module()```或者```__import__()```函数的形参。
- 此名称会在导入搜索的各个阶段被使用，它也可以是指向一个子模块的带点号路径，例如 foo.bar.baz。 在这种情况下，Python 会先尝试导入 foo，然后是 foo.bar，最后是 foo.bar.baz。 如果这些导入中的任何一个失败，都会引发 ModuleNotFoundError。

```python
>>> a = __import__('os')
>>> a
<module 'os' from '/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/os.py'>
>>> type(a)
<class 'module'>
```

- 这个时候，我们并没有导入```os```，只是新建一个```module```，并初始化了它。
当我们要通过 ```os```这个名称使用它时，需要我们绑定```{'os':a}```到命名空间。

```python
>>> a = __import__('os')
>>> globals()['os'] = a
>>> os
<module 'os' from '/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/os.py'>
```

> 2，当我们将 ```os```绑定到```globals```所代表的全局命名空间时，就可以直接调用它了。

> 注意：当```import```语句被执行时，标准的内置```__import__()```会被调用，其他发起调用导入系统的机制（比如```importlib.import_module()```）可能会选择**绕过**```__import__()```并使用它们自己的解决方案来实现导入机制。

  
### 首次导入：当一个模块被首词导入时，python 会搜索此模块，如果找到的话，就创建一个```module```对象并初始化它。如果没有找到的话，则会抛出```ModuleNotFoundError```。

```python
>>> import osss
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'osss'
```

### 命名空间：namespace

- 命名空间是存放变量的场所。
- 命名空间有局部、全局和内置的，还有对象中的嵌套命名空间（在方法之内）。
- 命名空间通过防止命名冲突来支持模块化。

> Python 是如何使用命名空间的呢？

#### 先来看下```python```解释器在命名空间中存放的内容

```python
python3
Python 3.7.1 (v3.7.1:260ec2c36a, Oct 20 2018, 03:13:28)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> globals()
{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>}
>>> import os
>>> globals()
{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, 'os': <module 'os' from '/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/os.py'>}
>>> type(globals())
<class 'dict'>
```

当我们导入```module```时，发现对应的命名空间```globals()```中已经记录了这个模块```os```和它对应的```key```:```os```。
而整个命名空间的存储形式为 ```dict```。

#### 下面我们看一下，定义的函数、变量在```globals()```中是如何存储的

> 函数：
定义了一个函数 ```test()```，它在```globals()```中为 ```'test': <function test at 0x100ac6730>```。

```python
>>> def test(a):
...     print(a)
...     return a
...
>>> globals()
{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, 'os': <module 'os' from '/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/os.py'>, 'test': <function test at 0x100ac6730>}
```

当我们输出 ```test```方法时，实际上也是在 ```globals()``` 去查找 ```test```的键值是否存在，当存在时，返回存储的```value```值。

```python
>>> type(test)
<class 'function'>
>>> test
<function test at 0x100ac6730>
>>> globals()['test']
<function test at 0x100ac6730>
```

而当我们调用 ```test```时，其实也是调用的```globals()['test']()```。其实对象可不可以执行，取决于它有没有实现 ```python```中定义的可以调用的```方法```。

```python
>>> globals()['test'](1)
1
1
```

> 变量：
定义了一个变量```a=1```。结果中也出现了存储的变量```'a':1```。

```python
>>> a = 1
>>> globals()
{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, 'os': <module 'os' from '/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/os.py'>, 'test': <function test at 0x100ac6730>, 'a': 1}
```

### 我们看下在自定义的模块和在模块中定义的方法和和变量的使用方式

首先定义了模块 ```test1```,下面是模块的内容，包含一个函数```test```和一个变量```a```。
```python
# test1.py
import os

def test():
    print(1)

a = 1

print(__name__)

if __name__ == "__main__":
    print(__name__)
    test()
```

下面我们尝试导入```test1```到```python```解释器主进程中。

```python
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import test1
test1
>>> type(test1)
<class 'module'>
>>> test1
<module 'test1' from '/Users/mengwei/workspace/mine/python_test/test1.py'>
```
通过 ```import``` 语句，我们导入了 ```test1``` 模块。可以看到```test1```的类型为```module``` ，绑定的值是```test1.py```文件。

现在，我们已经导入了```test1```，下面来看一下如何使用它。

```python
>>> test1.a
1
>>> test1.os
<module 'os' from '/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/os.py'>
>>> test1.test
<function test at 0x10e8a36a8>
```

当我们调用```test1```中定义的变量 ```a```时，发现是可以直接调用的。因为```a```和 ```test```都是定义在 ```test1``` 模块中的，所以我们可以直接使用导入后模块中定义的变量和方法，使用的是```test1.xxx```来调用的。

而在 ```test1```中导入的模块，我们也可以通过通过上述方法进行调用。

> 但是，```os```模块在```test1```中导入了，那我们可以直接在导入```test1```的主进程中使用它么？

```python
>>> os
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'os' is not defined
>>> test1.os
<module 'os' from '/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/os.py'>
```

> 答案当然是不可以。

因为导入```os```模块的是```test1```，所以在```test1```中的全局命名空间内```globals()```中存储了```{'os':<module ...>```，并可以通过 ```test1```调用。
但是在当前进程中，我们并没有```import os```，所以在```globals()```中只会存储```test1```，而不会有```os```相关的信息。

```python
>>> globals()
{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, 'a': 1, 'test1': <module 'test1' from '/Users/mengwei/workspace/mine/python_test/test1.py'>}
```

所以，需要我们将```os```在当前进程中再导入一次，才可以使用。那么```os```被导入了2次，会不会产生2个不同的模块呢？

```python
>>> test1.os
<module 'os' from '/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/os.py'>
>>> import os
>>> os
<module 'os' from '/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/os.py'>
>>> id(test1.os)
4537473368
>>> id(os)
4537473368
```

当然Python是不会导入2次相同模块的，当我们尝试再次导入之前已经导入的模块时，Python 解释器会去尝试导入，当发现已经存在此名称的模块已经导入时，则只是将已经导入的模块重新引入当前的命名空间，并绑定到导入的名称上去。
这样，我们就可以在不重复导入的情况下，使用模块。

> 但是，如果我们想更新某个已经导入的模块时，如何进行操作呢？

例如：我们想在已经导入的 ```test1```模块中添加一个变量```b```。

```python
b = "test on reload"
```

我们如何使用呢？

```python
Python 3.7.1 (v3.7.1:260ec2c36a, Oct 20 2018, 03:13:28)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import test1
test1
>>> id(test1)
4510694920
>>> test1.a
1
>>> test1.b
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: module 'test1' has no attribute 'b'
```

当我添加完成后，我们尝试去访问 ```b```，结果是没有找到，哪怕我们重新导入 ```test1```,也没法办法导入 ```b```，因为前面我们说过，当你重新导入一个已经被倒入过的模块时，是无法重新导入的，python 会因为效率直接使用之前已经导入的对象```module```。所以，我们需要使用```importlib.reload()```。

```python
>>> import importlib
>>> importlib.reload(test1)
test1
<module 'test1' from '/Users/mengwei/workspace/mine/python_test/test1.py'>
>>> id(test1)
4510694920
>>> test1.b
'test on reload'
```

使用 ```importlib.reload()``` 并不会重新生成一个新的对象，通过```id()```可以看到还是之前导入的```module```对象，但是更新了```module```对象的内容，而且导入的时候也执行了```print('test')```输出了 ```test```。


> 关于导入环

当我们在模块```a```中使用了 ```b.b_test```,又同时在```b```中使用了```a.a_test```模块，那么当你使用 ```a```或者```b```时，解释器就会告诉你出错。

```python
# a.py
from b import b_test
print(b_test)
a_test = 1
```

```python
# b.py
from a import a_test
print(a_test)
b_test = 2
```


```python
>>> import a
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/mengwei/workspace/mine/python_test/a.py", line 1, in <module>
    from b import b_test
  File "/Users/mengwei/workspace/mine/python_test/b.py", line 1, in <module>
    from a import a_test
ImportError: cannot import name 'a_test' from 'a' (/Users/mengwei/workspace/mine/python_test/a.py)
```

> 导入环是如何产生的呢？

1， 其实，当我们导入```a```模块时，它刚开始进行导入操作，结果 ```a```中引用了```b```模块的信息，而且是在 ```a```的最靠前的位置。现在 ```a module```已经被初始化，但是它的信息```__dict__```还是空的。

2， 导入系统现在去导入```b```模块，发现```b```的最靠前的位置，竟然是导入```a```。

3，然而，到现在为止，```a```模块什么操作都没有执行，所以```a_test```变量压根就没有被放置到```module a```的```__dict__```中去。

4，导入系统报错，```a```模块中发现没有 ```a_test```元素。

> 让我们稍微改动下代码，那么上述问题将不再出现，那就是在导入 ```b```之前执行```a_test```操作。

```python
# a.py
a_test = 1
from b import b_test
print(b_test)
```

现在，我们执行一下导入操作，可以顺利导入 ```a```模块。这时的 ```b```模块已经在```a```中被导入，所以没有出错。

```python
>>> import a
1
2
>>> import b
```

然而，```b```模块如果被初次导入的话，还是会像之前一样，因为 ```a```模块在 ```b```模块定义 ```b_test```的语句执行之前，就导入了```b_test```。

```python
>>> import b
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/mengwei/workspace/mine/python_test/b.py", line 1, in <module>
    from a import a_test
  File "/Users/mengwei/workspace/mine/python_test/a.py", line 2, in <module>
    from b import b_test
ImportError: cannot import name 'b_test' from 'b' (/Users/mengwei/workspace/mine/python_test/b.py)
```


所以有时候，在写代码的时候，经常会出现先导入```a```就正常，先导入```b```就失败报错，这下大家明白问题出在那里了吧。


> 关于 global，local 关键字，__name__ ，import，from import，导入路径搜索优先级等，将在后面的章节进行说明。

