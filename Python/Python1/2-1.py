## 自定义序列


class MySeq(object):
    def __init__(self, temp=None):
        self.data = [temp]
        pass

    def __add__(self, l):
        for i in l.data:
            self.data.append(i)
        return self

    def __len__(self):
        return len(self.data)

    def __reversed__(self):
        return self.data.reverse()

    def __count__(self, i):
        return self.data.count(i)

    def __str__(self):
        return self.data.__str__()

    def __getitem__(self, item):
        return self.data[item]


if __name__ == "__main__":
    m = MySeq(1)
    m1 = MySeq(1)
    print(len(m))
    m += m1
    print(m)
    print(len(m))
    print(m[1])
