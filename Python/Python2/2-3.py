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
