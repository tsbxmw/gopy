## 闭包


def test_1():
    temp = []
    temp_1 = 1

    def test():
        temp.append(temp_1)
        return temp
    return test


func = test_1()

print(func())
print(func())
print(func())
