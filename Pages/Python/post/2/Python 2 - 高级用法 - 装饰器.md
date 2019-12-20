# Python 2 - 高级用法 - 装饰器

> 一谈到 装饰器，就离不开```闭包```

## 闭包

> 闭包就是能够读取其他函数内部变量的函数。这个被引用的自由变量将和这个函数一同存在，即使已经离开了创造它的环境也不例外。

### 作用域

> 了解 闭包之前，先来看一下作用域

作用域是程序运行时变量可被访问的范围，定义在函数内的变量是局部变量，局部变量的作用范围只能是函数范围内，它不能在函数外引用。当函数结束时，变量也会跟随函数结束而变得不可以被访问。

[source](https://github.com/tsbxmw/gopy/blob/master/Python/Python2/1-1.py)
```python

## 作用域
def test_1():
    test = 1

test_1()
print(test)
```

```shell
/gopy # python Python/Python2/1-1.py
Traceback (most recent call last):
  File "Python/Python2/1-1.py", line 10, in <module>
    print(test)
NameError: name 'test' is not defined
```

当你在 ```test_1()``` 函数外部尝试访问作用域中的变量 ```test``` 时，此时 Python解释器会向你报告错误信息： ```NameError: name 'test' is not defined```。说明此时的 ```test``` 变量并不能在```test_1()```外部被访问到。

### 闭包

> 你在函数 A 中定义了 函数 B，并将 B 作为 A 的返回值返回， B 又使用了 A 中定义了的 变量，此时，可以形成了闭包。

```python
# 闭包的形式
def A():
     a = 1
     def B():
          print(a)
     return B
```

> 下面的例子说明了闭包
当 ```test()``` 函数 和 ```temp = []``` 变量离开了定义它的函数 ```test_1()```后，依然可以被 ```test()```所保留。

[source](https://github.com/tsbxmw/gopy/blob/master/Python/Python2/1-2.py)
```python
## 闭包
def test_1():
    temp = []
    t = 1
    # 定义在函数内部的函数

    def test():
        temp.append(t)  # 使用了上层 test_1 中定义的局部变量：temp
        print(f"{temp}.append({t})")
    return test  # 注意，这里返回的是 test 函数


func = test_1()  # 这里获取 test_1 中定义的 test

func()  # 这里可以看到 test_1 的局部变量 temp 变成了 [1]
func()  # 说明可以通过 test 去访问 temp 变量 和 t 变量
func()

```

```shell
# 输出
/gopy # python Python/Python2/1-2.py
[1].append(1)
[1, 1].append(1)
[1, 1, 1].append(1)
```

所以，函数 ```test()``` 是如何知道变量 ```temp``` 和 ```t``` 的呢？原来在 ```test``` 的属性中存在了一个用来存储相关内容的列表 ```__closure__```。

```python
for i in func.__closure__:
    print(i.cell_contents)
```

这下我们可以看到 闭包 通过 ```__closure__``` 将 函数 ```test``` 与 变量 ```temp``` 和 ```t``` 绑定在了一起。

```shell
1
[1, 1, 1]
```

## 装饰器

了解了闭包，装饰器就很好理解了。装饰器其实是闭包的一种特殊形式。

### 原始工作

现在有一个工作方法```work```，用来输出工作状态```i am working...``` 并返回 100.

[source](https://github.com/tsbxmw/gopy/blob/master/Python/Python2/1-3.py)
```python
## 工作中
def work():
    work_time = 100
    print('i am working ...')
    return work_time
```
```shell
gopy # python Python/Python2/1-3.py
i am working ...
```

这时，突然你想增加一个功能，统计```work``` 的实际工作时间，最简单的方法是更改 work 的源码，增加计算时间的代码。

```python
## 计算时间的工作
import time

def work_1():
    work_time = 100
    start = time.time()
    print('i am working ...')
    stop = time.time()
    print(f'working time is : {stop - start}')
    return work_time
```

```shell
i am working ...
working time is : 2.5272369384765625e-05
```

这只是只有一个 ```work``` 的情况，如果有几十个上百个 ```work```的话，也要每个都去改吗？这时，装饰器上线了！

```python
## 装饰器：计算时间
import time

def work_time_cal(func):  # 定义装饰器，func 为变量
    def wrap():  # 装饰器内部闭包函数
        start = time.time()
        result =func()  # 运行 func
        stop = time.time()
        print(f'working time is : {stop - start}')
        return result
    return wrap  # 返回闭包函数

## 工作中
@work_time_cal  ## python 中的装饰器语法为 @ + 装饰器名称
def work_2():
    work_time = 100
    print('i am working 2 ...')
    return work_time
```

我们打印下```work_2```：

```python
print(work_2)
# <function work_time_cal.<locals>.wrap at 0x10314e510>
```

果然，```work_2```竟然变成了```work_time_cal.wrap```！说明 装饰器 @ 起作用了，那我们来看下它的 ```__closure__```中绑定的是什么？
```python
print(work_2.__closure__[0].cell_contents)
# <function work_2 at 0x10314e6a8>
```
原来是我们的 ```work_2```。也就是 ```@work_time_cal``` 把 ```work_2``` 作为 ```func``` 传入了 ```wrap```。最后 ```work_2``` 查看的时候变成了 ```wrap```。

那这个时候，我们运行 ```work_2``` 的话，其实运行的是 ```wrap()``` 闭包。而 ```wrap``` 计算了开始结束时间，并输出，然后返回了 ```work_2``` 的结果。

```python
 def wrap():  # 装饰器内部闭包函数
        start = time.time()
        result =func()  # 运行 func
        stop = time.time()
        print(f'working time is : {stop - start}')
        return result
```

```shell
i am working 2 ...
working time is : 5.7220458984375e-06
```

效果是不是与在函数中直接修改是一样的？所以 装饰器是一种在不改变原有函数内部代码的情况下，增加功能的一种方法。

现在，我们也发现了，其实 @ + 装饰器的作用是，将 下面的函数名作为参数，传到了装饰器中，作为装饰器的参数。

### 类装饰器

类具有一个方法``` __call__```,只要实现了这个方法的，那么这个类的实例都是可以被调用的。python 中万物皆对象，所以我们来看下平时使用的方法有没有 ```__call__``` 呢，他也时可调用的。

```python
>>> def test():
...           print()
... 
>>> dir(test)
['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
>>> test.__call__
<method-wrapper '__call__' of function object at 0x7fd009e71bf8>
```
我们在 ```test``` 中的属性中看到了```__call__```方法，他是一个 method-wrapper 类型。那么我们调用``` test()``` 的时候，实际上调用的也是 ```test.__call__()```。所以通过 ```__call__``` 提供了类作为装饰器的方法。

类装饰器的实现实际上是通过 ```__init__``` 在创建的时候传入被装饰函数作为参数，创建类的实例，然后类具有的 ```__call__``` 作为实际运行的方法。

```python
class WorkTimeCal12(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print(args)
        print(**kwargs)
        return self.func()

@WorkTimeCal12
def work_12():
    return 100
```

这里的 @WorkTimeCal12 其实执行的是 WorkTimeCal12(work_12)，最后获得的实例 self.func = work_12。
所以我们来看下 被装饰后的```work_12``` 是什么类型呢？

```python
>>> print(work_12)
<test.WorkTimeCal12 object at 0x7fd009e9b2b0>
```

是 WorkTimeCal12 d的实例对象，所以运行的是这个对象的```__call__```。它即等同于以下代码：

```python
def work_13():
    return 100

worktimecal12 = WorkTimeCal12(work_13)
worktimecal12()
```

### 带参数的类装饰器类型

> 被装饰方法不带参数，类装饰器带参数


```python
# 类装饰器，装饰器带参数，方法不带参数

class WorkTimeCal13(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print(args)
        print(**kwargs)
        return self.func()

@WorkTimeCal13
def work_13():
    return 100

work_13()
print(work_13)
```


### 多个装饰器的叠加使用与运行次序

> 多个装饰器的叠加使用

```python
# 多个装饰器叠加

def test1(func):
    def wrap():
        print("i am test 1 begin")
        rev = func()
        print("i am test 1 end")
        return rev
    return wrap


def test2(func):
    def wrap():
        print("i am test 2 begin")
        rev = func()
        print("i am test 2 end")
        return rev
    return wrap

@test1
@test2
def test_3():
    print("i am test 3")

test_3()
```

```shell
<function test1.<locals>.wrap at 0x1074b5a60>
i am test 1 begin
i am test 2 begin
i am test 3
i am test 2 end
i am test 1 end
```

> 多个装饰器的运行次序是什么呢？

通过结果可以看到，实际的运行是这样的：

```python
test_1 begin
    test_2 begin
         test_3 begin - end
    test_2 end
test_1 end
```

所以，叠加装饰器，实际上是离方法最近的装饰器 ```test_2```，在装饰完方法 ```test_3```后，返回的 ```test_2.wrap``` 又被 ```test_1```装饰，返回了 ```test_1.wrap```。

由此可知，叠加装饰器的运行次序实际上是由最外层的装饰器依次向内部运行，最后执行被装饰的方法。

### functools.wrap

被装饰的方法被修改了成了装饰器方法的返回值，那么如何保留之前的方法属性呢？答案就是 ```functools.wrap``` 装饰器

```python
# functools.wrap
import functools

def testfunc(func):
    @functools.wraps(func)
    def wrap():
        return func()
    return wrap

@testfunc
def test_wrap():
    print('test wrap')

print(test_wrap)
test_wrap()
```

```shell
<function test_wrap at 0x10fc9dbf8>
test wrap
```

那么这个名称相同的函数，还是原来的函数么？

```python
print(test_wrap)
#<function test_wrap at 0x103d47bf8>

print(test_wrap.__closure__[0].cell_contents)
#<function test_wrap at 0x103d47b70>
```

它们并不相同，原来是名字修改成了被装饰函数名， ```__closure__```存储的还是被装饰函数。

## 其他类型的装饰器

### 带有确定参数的装饰器

>  注意，固定参数和不定参数的区别只是形式问题，只要正常传入即可，结构都是相同的

#### 装饰器无参数，被装饰的函数有固定的参数

[source](https://github.com/tsbxmw/gopy/blob/master/Python/Python2/1-4.py)

```python
## 装饰器：计算时间 - 被装饰的函数有参数:固定参数，装饰器无参数
def work_time_cal_2(func):
    def wrap(param1, param2):  # 装饰器内部闭包函数，带两个固定参数
        start = time.time()
        result = func(param1, param2)  # 运行 func
        stop = time.time()
        print(f'working time is : {stop - start}')
        return result
    return wrap  # 返回闭包函数

@work_time_cal_2
def work_2(param1, param2):
    print(f"params is {param1} and {param2}")
    return 100

work_2(123, 245)

#params is 123 and 245
#working time is : 1.2874603271484375e-05
```

#### 装饰器有固定参数，被装饰的函数没有参数

```python
## 装饰器：计算时间 - 被装饰的函数没有参数，装饰器有参数：固定参数
def work_time_cal_4(param1):
    print(f"work time cal 4's params is : {param1}")
    def wrap_func(func): # 装饰器内部闭包函数 1 : 参数是 func
        def wrap():  # 装饰器内部闭包函数 2 : 运行的是具体的 func
            start = time.time()
            result = func()  # 运行 func
            stop = time.time()
            print(f'working time is : {stop - start}')
            return result
        return wrap  # 返回闭包函数 2
    return wrap_func  # 返回闭包函数 1

@work_time_cal_4(1)
def work_4():
    return 100

work_4()

#work time cal 4's params is : 1
#working time is : 9.5367431640625e-07
```

#### 装饰器有固定参数，被装饰的函数也有固定参数

```python
## 装饰器：计算时间 - 被装饰的函数有参数：固定参数，装饰器有参数：固定参数
def work_time_cal_6(param1):
    print(f"work time cal 6's params is : {param1}")
    def wrap_func(func): # 装饰器内部闭包函数 1 : 参数是 func
        def wrap(in1, in2):  # 装饰器内部闭包函数 2 : 运行的是具体的 func
            print(f"work time cal 6-wrap's params is {in1} and {in2}")
            start = time.time()
            result = func(in1, in2)  # 运行 func
            stop = time.time()
            print(f'working time is : {stop - start}')
            return result
        return wrap  # 返回闭包函数 2
    return wrap_func  # 返回闭包函数 1

@work_time_cal_6(1)
def work_6(in1, in2):
    return in1 + in2

work_6(1, 2)

#work time cal 6's params is : 1
#work time cal 6-wrap's params is 1 and 2
#working time is : 1.1920928955078125e-06

```


### 带有不确定参数的装饰器

#### 装饰器无参数，被装饰的函数有固定参数

```python
## 装饰器：计算时间 - 被装饰的函数有参数:不固定参数，装饰器无参数
def work_time_cal_3(func):
    def wrap(*args, **kwargs):  # 装饰器内部闭包函数，带不固定参数
        start = time.time()
        result = func(*args, **kwargs)  # 运行 func
        stop = time.time()
        print(f'working time is : {stop - start}')
        return result

    return wrap  # 返回闭包函数

@work_time_cal_3
def work_3(*args, **kwargs):
    print(f"params is {args} and {kwargs}")
    return 100
#params is (1, 2, 3, 4, 5) and {'p': -1, 'p1': -2}
#working time is : 1.3113021850585938e-05
```

#### 装饰器有不固定参数，被装饰的函数无参数

```python
## 装饰器：计算时间 - 被装饰的函数无参数，装饰器有参数：不固定参数
def work_time_cal_5(*args, **kwargs):
    print(f"work time cal 5's params is : {args} and {kwargs}")
    def wrap_func(func): # 装饰器内部闭包函数 1 : 参数是 func
        def wrap():  # 装饰器内部闭包函数 2 : 运行的是具体的 func
            start = time.time()
            result = func()  # 运行 func
            stop = time.time()
            print(f'working time is : {stop - start}')
            return result
        return wrap  # 返回闭包函数 2
    return wrap_func  # 返回闭包函数 1

@work_time_cal_5(1, 2, 3, 4, p=1, p1=2)
def work_5():
    return 100

work_5()
#work time cal 5's params is : (1, 2, 3, 4) and {'p': 1, 'p1': 2}
#working time is : 7.152557373046875e-07
```

### 类方法装饰器

#### 类方法装饰器不带参数，类方法不带参数

```python
# 装饰器：类方法装饰器，类方法不带参数
def work_time_cal_8(func):  # 带有 self 来表示 类
    def wrap(self):  # 其实这里 self 也是参数，只不过是 类的 self,他也可以叫别的名字，只要位于第一位参数即可
        start = time.time()
        result = func(self)  # 运行 func 时也是调用 func(self)
        stop = time.time()
        print(f'class working time is : {stop - start}')
        return result
    return wrap

class A(object):
    def __init__(self):
        pass

    @work_time_cal_8
    def work_8(self):
        return 100

a=A()
a.work_8()
```

#### 类方法装饰器不带参数，类方法带参数:固定参数

```python

# 装饰器：类方法装饰器，类方法带参数
def work_time_cal_9(func):  # 带有 self 来表示 类
    def wrap(self, param1, param2):  # 其实这里 self 也是参数，只不过是 类的 self,他也可以叫别的名字，只要位于第一位参数即可
        print(f'work time cal 9-wrap param is  : {param1} and {param2}')
        start = time.time()
        result = func(self, param1, param2)  # 运行 func 时也是调用 func(self),后面跟参数即可
        stop = time.time()
        print(f'class working time is : {stop - start}')
        return result
    return wrap

class B(object):
    def __init__(self):
        pass

    @work_time_cal_9
    def work_9(self, param1, param2):
        return 100

a=B()
a.work_9(1, 2)
```

#### 装饰器方法带参数，类方法不带参数

```python
# 装饰器：装饰器方法带参数，类方法不带参数
def work_time_cal_10(param1, param2):  # 带有 self 来表示 类
    print(f"work time cal 10's param is {param1} and {param2}")
    def wrap_class(func):
        def wrap(self):  # 其实这里 self 也是参数
            start = time.time()
            result = func(self)  # 运行 func 时也是调用 func(self)
            stop = time.time()
            print(f'class working time is : {stop - start}')
            return result
        return wrap
    return wrap_class


class C(object):
    def __init__(self):
        pass

    @work_time_cal_10(1, 2)
    def work_10(self):
        return 100

c=C()
c.work_10()
```

#### 装饰器方法带参数，类方法带参数,都是不定参数

```python
# 装饰器：装饰器方法带参数，类方法带参数,都是不定参数
def work_time_cal_11(*args, **kwargs):  # 带有 self 来表示 类
    print(f"work time cal 10's param is {args} and {kwargs}")
    def wrap_class(func):
        def wrap(self, *args1, **kwargs1):  # 其实这里 self 也是参数
            start = time.time()
            result = func(self, *args1, **kwargs1)  # 运行 func 时也是调用 func(self)
            stop = time.time()
            print(f'class working time is : {stop - start}')
            return result
        return wrap
    return wrap_class

class D(object):
    def __init__(self):
        pass

    @work_time_cal_11(1, 2, p=1, p1=2)
    def work_11(self, *args, **kwargs):
        print(f"work 11's params is {args} and {kwargs}")
        return 100

d = D()
d.work_11(3, 4, p=123, p1=234)
```


