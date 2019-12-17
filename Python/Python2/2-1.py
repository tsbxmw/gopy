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
        return super(StrSub, cls).__new__(cls, test)


if __name__ == "__main__":
    ss = StrSub("test")