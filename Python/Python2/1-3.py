## 装饰器


## 工作中
def work():
    work_time = 100
    print('i am working 1 ...')
    return work_time


work()

## 计算时间的工作
import time


def work_1():
    work_time = 100
    start = time.time()
    print('i am working 1 ...')
    stop = time.time()
    print(f'working time is : {stop - start}')
    return work_time


work_1()

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

print(work_2)
# <function work_time_cal.<locals>.wrap at 0x10314e510>

print(work_2.__closure__[0].cell_contents)
# <function work_2 at 0x10314e6a8>

work_2()

