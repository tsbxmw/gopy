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
    print(B.__mro__)
    print(B.__dict__)
    print(A.__dict__)
    a = A()
    print(a.a)
    print(type(a))

    print(type(A))
    print(type(B))
