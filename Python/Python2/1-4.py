import time


## 注意，固定参数和不定参数的区别只是形式问题，只要正常传入即可，结构都是相同的

## 装饰器：计算时间 无参数
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
def work_1():
    work_time = 100
    print('i am working 2 ...')
    return work_time


work_1()


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


work_3(1, 2, 3, 4, 5, p=-1, p1=-2)


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


## 装饰器：计算时间 - 被装饰的函数有参数：不固定参数，装饰器有参数：不固定参数
def work_time_cal_7(*args, **kwargs):
    print(f"work time cal 7's params is : {args} and {kwargs}")
    def wrap_func(func): # 装饰器内部闭包函数 1 : 参数是 func
        def wrap(*args1, **kwargs1):  # 装饰器内部闭包函数 2 : 运行的是具体的 func
            print(f"work time cal 7-wrap's params is : {args} and {kwargs}")
            start = time.time()
            result = func(*args1, **kwargs1)  # 运行 func
            stop = time.time()
            print(f'working time is : {stop - start}')
            return result
        return wrap  # 返回闭包函数 2
    return wrap_func  # 返回闭包函数 1


@work_time_cal_7(1, 2, 3, 4, p=1, p1=2)
def work_7(*args, **kwargs):
    return 100


work_7(1,2,3,4, p=1, p1=2)


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


# 装饰器：类方法装饰器，类方法带参数：
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


# 类装饰器，装饰器不带参数，方法不带参数

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

print(work_12())
print(work_12)


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