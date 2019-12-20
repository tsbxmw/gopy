class A(object):
    pass

class B(object):
    pass

class C(A, B):
    pass

class D(A):
    pass

class E(D, C):
    pass

print(A.mro())
print(B.mro())
print(C.mro())
print(D.mro())
print(E.mro())