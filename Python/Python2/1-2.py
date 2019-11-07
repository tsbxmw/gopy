## 闭包
def test_1():
    temp = []
    # 定义在函数内部的函数

    def test():
        temp.append(1)  # 使用了上层 test_1 中定义的局部变量：temp
        print(temp)
    return test


func = test_1()  # 这里获取 test_1 中定义的 test

func()  # 这里可以看到 test_1 的局部变量 temp 变成了 [1]
func()  # 说明可以通过 test 去访问 temp 变量
func()