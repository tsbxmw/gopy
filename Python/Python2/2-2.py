class UpperStr(str):
    def __init__(self, string):
        print("__init__ begin")
        self.test = string
        print(self.test)
        print("__init__ over")

    def __new__(cls, string):
        print("__new__ begin")
        print(cls)
        print(string)
        print("__new__ over")
        string = string.upper()
        return super(UpperStr, cls).__new__(cls, string)


if __name__ == "__main__":
    ss = UpperStr("test")
    print(ss)
    print(type(ss))