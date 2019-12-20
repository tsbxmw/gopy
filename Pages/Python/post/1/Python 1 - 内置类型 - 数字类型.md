# Python 内置类型 - 数字类型

# 数字类型

> Python 中存在三种不同的数字类型，包括整数 ```int``` 和 浮点数 ```float``` 和 复数 ```complex```。
(注意 - 布尔值也是整数的子类型)

## 数字的初始化

> 数字是由数字字面值或内置函数与运算符的结果来创建的

### 初始化 ```int``` 类型

> 不带修饰的整数字面值（包括十六进制、八进制和二进制数）会生成整数

```python
a = 1
# 1，十进制
a = 0x11
# F + 1 = 17，十六进制
a = 0b11
# 2 + 1 = 3，二进制
```

> 负数也是整数

```python
a = -1
# -1
```

> 内置函数 ```int()``` 可以初始化和转换别的类型为整数

```python
a = int()
# 0
a = int(1)
# 1
a = int('1')
# 1
```


### 初始化 ```float``` 类型 

> 包含小数点（或幂运算符,存疑）的数字字面值会生成浮点数

```python
b = 1.0
# 1.0
b = 10**2
# 100, 存疑
```

> 内置函数 ```float()``` 可以初始化和转化别的类型为浮点类型

```python
b = float()
# 0.0
b = float(1)
# 1.0，整数转化为浮点数
```

> ```math.pow(x,y)``` 可以返回```幂结果```为浮点类型

```python
b = math.pow(10,2)
# 100.0
```

### 初始化生成复数 ```complex``` 

- 在数字字面值末尾加上 'j' 或 'J' 会生成虚数（实部为零的复数）

```python
c = complex()
# 0j，实部为 0，虚部为 0j
c = complex(1,2)
# 1+2j，实部为 1，虚部为 2j
c = 1+2j
# (1+2j)
```

# 数字类型之间的运算

> Python 支持数字类型之间的混合运算，运算规则如下：

- 当一个二元运算符用于不同数字类型的操作数时，具有“较窄” 类型的操作数会被扩展为另一个操作数的类型。
- 整数比浮点数更窄，浮点数又比复数更窄。
- 混合类型数字之间的比较也使用相同的规则。

```python
a = 1
# int
b = 1.0
# float
c = 1+2j
# complex
d = a+b
# 2.0, float
e = a+c
# 2+2j, complex
f = a+b+c
# 3+2j, complex
```

## 数字类型运算

### 通用运算

- a+b, a-b,  a*b, a/b
- 整除 ```//```，运算结果总是舍掉不足整数的部分。
```python
1//2 ==> 0.5 ==> 0
(-1)//2 ==> -0.5 ==> -1
```
- 取余 ```%```
```python
10%3 ==> 1
```
- 取负数 ```-```
- 绝对值 ```abs(-1)``` == ```1```
- 除数和余数 ```divmod(10,3)``` >>> ```(3, 1)```
- 幂级数计算
```python
pow(3,2)
# 3^2 = 9
3 ** 2
# 9
```

### 整数类型位运算

> 位运算是将整数转为二进制数后，按位进行运算

- 或 ```|``` 运算
```python
4 | 1
# 4: 100
# 1:  001
# 5:  101
```
- 与```&```运算
```python
4 & 1
# 4: 100
# 1:  001
# 0: 000
```
- 异或```^```运算
```python
4 ^ 1
# 4 : 100
# 1 :  001
# 5:   101
```
- 左移```<<```运算,左移带来的是 2^n 次幂与原数的乘积
```python
4 << 1
# 4 : 0100
#      1000
# 8:  4 * 2^1
```
- 左移```<<```运算,左移带来的是 2^n 次幂与原数的商
```python
4 >> 1
# 4 : 0100
#      0010
# 2 : 4 / 2^1
```

### 哈希运算

> 哈希算法的实质是对原始数据的有损压缩，有损压缩后的固定字长用作唯一标识原始数据。
对于不同类型的数字 ```a``` 和 ```b```,当 ```a==b``` 时， ```hash(a)==hash(b)```。
对于 ```hash```,我们后面再进行展开。

# 源码解析

## int

> Python 中的 ```int``` 其实是 C 中的 ```long int``` 类型。
我们可以在文件```longobject.c```的开头看到以下描述。

```c
/* Long (arbitrary precision) integer object implementation */

/* XXX The functional organization of this file is terrible */
```

### 定义 & 初始化

#### 定义

> Python 中定义了 存储数据的对象 ```PyLongObject```

![](https://images.xiaozhuanlan.com/photo/2019/ae59000cf2fb405a68bdbb9852ebd996.png)

- 在文件 ```longobject.h``` 中定义了 结构体 ```PyLongObject```

```c
/* Long (arbitrary precision) integer object interface */
typedef struct _longobject PyLongObject; /* Revealed in longintrepr.h */
```
- 在文件 ```longintrepr.h``` 定义了 ```_longobject```

```c
struct _longobject {
    PyObject_VAR_HEAD
    digit ob_digit[1];
};
```
- 可以看到 使用了数组来存储真正的数值：```ob_digit```, 看下它的定义是什么：
```c
值为：
val = 0
for i=0;i<abs(ob_size); i++ :
    val += ob_digital[i] * 2^(SHIFT*i)
负数的话， ob_size < 0, 所以使用 绝对值；
0 的 ob_size = 0
/*
   Long integer representation.
   The absolute value of a number is equal to
        SUM(for i=0 through abs(ob_size)-1) ob_digit[i] * 2**(SHIFT*i)
   Negative numbers are represented with ob_size < 0;
   zero is represented by ob_size == 0.
   In a normalized number, ob_digit[abs(ob_size)-1] (the most significant
   digit) is never zero.  Also, in all cases, for all valid i,
        0 <= ob_digit[i] <= MASK.
   The allocation function takes care of allocating extra memory
   so that ob_digit[0] ... ob_digit[abs(ob_size)-1] are actually available.

   CAUTION:  Generic code manipulating subtypes of PyVarObject has to
   aware that ints abuse  ob_size's sign bit.
*/
```
- 而 ```PyObject_VAR_HEAD```的定义存储了可变部分元素的数量。
```c
typedef struct {
    PyObject ob_base;
    Py_ssize_t ob_size; /* Number of items in variable part */
} PyVarObject;
```
- 关于此类型```PyLong_Type```定义了与```int```相关的属性
```c
PyTypeObject PyLong_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "int",                                      /* tp_name */
    offsetof(PyLongObject, ob_digit),           /* tp_basicsize */
    sizeof(digit),                              /* tp_itemsize */
    long_dealloc,                               /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_reserved */
    long_to_decimal_string,                     /* tp_repr */
    &long_as_number,                            /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    (hashfunc)long_hash,                        /* tp_hash */
    0,                                          /* tp_call */
    long_to_decimal_string,                     /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE |
        Py_TPFLAGS_LONG_SUBCLASS,               /* tp_flags */
    long_doc,                                   /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    long_richcompare,                           /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    long_methods,                               /* tp_methods */
    0,                                          /* tp_members */
    long_getset,                                /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    0,                                          /* tp_init */
    0,                                          /* tp_alloc */
    long_new,                                   /* tp_new */
    PyObject_Del,                               /* tp_free */
};
```
#### 初始化

> 上面代码```PyLong_Type```中的```tp_new``` : ```long_new```定义了初始化一个 int 对象的的方法。

![](https://images.xiaozhuanlan.com/photo/2019/e2a1897c7b9bd38409cf3996d2e78fbc.png)

- python 中初始化一个 ```int```

```python
int(1, 10)
int(1)
int()
int.__new__(int, 1, 10)
```


> 在 python ```long_new``` 中既是 ```int.__new__```。
 ```int.__new__(int, value, base)``` 是 ```<class 'builtin_function_or_method'>``` 类型，所以 ```int.__new__(int, value, base)``` 就是 ```int(value, base) ```调用的就是 ```long_new(PyLong_Type, value, base)```

- 而```long_new``` 又调用了 ```long_new_impl```，下面我们看源码。

```c

static PyObject *long_new_impl(PyTypeObject *type, PyObject *x, PyObject *obase)
{
    Py_ssize_t base;
    // 判断传入的是不是 PyLong_type,不是的话使用 subtype 去创建
    if (type != &PyLong_Type)
        return long_subtype_new(type, x, obase); /* Wimp out */
  
    if (x == NULL) {   // ①这里传入的要转换的 PyObject 如果是 NULL， 后面会返回 0
        if (obase != NULL) {    //②这里如果要转换的类型是 NULL 且 传入的 PyObject 是 NULL，后面会抛出错误：“int() missing string argument”
            PyErr_SetString(PyExc_TypeError,
                            "int() missing string argument");
            return NULL;
        }
        return PyLong_FromLong(0L); // ①使用 PyLong_FromLong(0L) 去返回 PyLongObject(0)对象的 digital[0] == 0
    }
    if (obase == NULL) {  // ③如果只有要转换的类型是 NULL，则默认 base=10进制
        return PyNumber_Long(x); // ③ 通过 PyNumber_Long() 转换为 PyLongObject
    }

    base = PyNumber_AsSsize_t(obase, NULL); // 这里转换 base，如果出错了会返回 -1
    if (base == -1 && PyErr_Occurred()) // 如果 出错了直接返回 NULL
        return NULL;
    if ((base != 0 && base < 2) || base > 36) {  // 如果 2<=base<=36 或者 base!=0 则报错
        PyErr_SetString(PyExc_ValueError,
                        "int() base must be >= 2 and <= 36, or 0");
        return NULL;
    }

    if (PyUnicode_Check(x)){  // 检查传入的 x 是不是 str（python3 中的 str 都是 unicode）
        return PyLong_FromUnicodeObject(x, (int)base);  // 直接使用 PyLong_fomUnicodeObject(x, int(base)) 将 x 转换为 base进制的 PyLongObject
    }
    else if (PyByteArray_Check(x) || PyBytes_Check(x)) {  // 如果不是 str 的话，要检查是不是 bytearray 或者 bytes 类型
        char *string;
        if (PyByteArray_Check(x))
            string = PyByteArray_AS_STRING(x); // 如果是 bytearray 类型的话， 通过 PyByteArray_AS_STRING(x) 转换 x 为 str 类型
        else
            string = PyBytes_AS_STRING(x); // 如果是  bytes 类型的话，通过 PyBytes_AS_STRING(x) 转换 x 为 str
        return _PyLong_FromBytes(string, Py_SIZE(x), (int)base);  // 在通过 PyLong_FromBytes 转换为 PyLongObject 返回
    }
    else {
        PyErr_SetString(PyExc_TypeError,
                        "int() can't convert non-string with explicit base");
        return NULL;
    }
}

```

- 下面我们通过一个函数```PyLong_FromLong(long vial)```，查看 ```int``` 是如何在内存中创建的

```c

/* Create a new int object from a C long int */
/* 从一个 C 类型的 long int 创建一个 int 类型 */
PyObject *PyLong_FromLong(long ival)
{
    PyLongObject *v;     // 声明一个 PyLongObject 
    unsigned long abs_ival;  // 创建一个 C 无符号long类型用来存储 ival 的绝对值
    unsigned long t;  /* unsigned so >> doesn't propagate sign bit */ // 因为是无符号数，所以不提供 符号位
    int ndigits = 0;  
    int sign;  // 标记位，0为0；1为整数；-1为负数

// 由下面的小数定义可以看到空间为 ： -5<=x<257 即 [-5, 256]
/* Small integers are preallocated in this array so that they can be shared、The integers that are preallocated are those in the range   -NSMALLNEGINTS (inclusive) to NSMALLPOSINTS (not inclusive).*/
// #define NSMALLPOSINTS           257  
// #define NSMALLNEGINTS           5
    if (IS_SMALL_INT(ival)) {  // 这里判断是不是 小数,下面是小数的定义：小数是提前 申请的，所以可以被共享。
        return get_small_int((sdigit)ival);
    }
// 之前的版本 CHECK_SMALL_INT
/*#define CHECK_SMALL_INT(ival) \
    do if (-NSMALLNEGINTS <= ival && ival < NSMALLPOSINTS) { \
        return get_small_int((sdigit)ival); \
    } while(0)
*/

    if (ival < 0) {  // 如果小于0，即是负数，则不能直接写入，需要计算 绝对值为 0 - ival，并将 标记记为 -1，表示负数
        /* negate: can't write this as abs_ival = -ival since that
           invokes undefined behaviour when ival is LONG_MIN */
        abs_ival = 0U-(unsigned long)ival;
        sign = -1; // 标记记为 -1，表示负数
    }
    else {
        abs_ival = (unsigned long)ival;  // 如果 大于0，则为整数，则绝对值为 ival
        sign = ival == 0 ? 0 : 1;  // 如果 ival 为 0，则标记记为 0，因为 0 是无符号的；而正是符号的标记记为 1
    }

    /* Fast path for single-digit ints */ 
    /* 如果是 单字 的数字 : 2个字节, 即绝对值 在 2^15 之间 */
   // #define PyLong_SHIFT    15
    if (!(abs_ival >> PyLong_SHIFT)) {  // 这里通过将数字右移 15 位 判断是不是单字数字
        v = _PyLong_New(1);  // 初始化一个 单字的内存，查看后面的 _PyLong_New 解析,v 是 PyLongObject
        if (v) {
            Py_SIZE(v) = sign;  // 这里是赋值 PyVarObject -> ob_size = sign
            v->ob_digit[0] = Py_SAFE_DOWNCAST(
                abs_ival, unsigned long, digit);  // 这里进行了强制类型转换
        }
        return (PyObject*)v;
    }

#if PyLong_SHIFT==15
    /* 2 digits */
   // 双字的数字
    if (!(abs_ival >> 2*PyLong_SHIFT)) {  // 双字的数字
        v = _PyLong_New(2); // 初始化两个字的内存
        if (v) {
            Py_SIZE(v) = 2*sign;  // 标志位需要 2*sign
            v->ob_digit[0] = Py_SAFE_DOWNCAST(  
                abs_ival & PyLong_MASK, unsigned long, digit); // 强行转换 abs_ival 的高 15 位置 0
//#define PyLong_BASE     ((digit)1 << PyLong_SHIFT)
//#define PyLong_MASK     ((digit)(PyLong_BASE - 1))  // ==> 100000000000000 -1 == 111111111111111
            v->ob_digit[1] = Py_SAFE_DOWNCAST(
                  abs_ival >> PyLong_SHIFT, unsigned long, digit); // 这里 abs_ival 右移 15位，将低位消除
        }
        return (PyObject*)v;
    }
#endif

    /* Larger numbers: loop to determine number of digits */
   // 大数，没有限制，根据数字来决定
    t = abs_ival;
    while (t) {
        ++ndigits;  // 需要多少字就申请多少字内存
        t >>= PyLong_SHIFT;   // 每次右移 15 位，存储为一个字
    }
    v = _PyLong_New(ndigits); // 申请内存
    if (v != NULL) {
        digit *p = v->ob_digit;  
        Py_SIZE(v) = ndigits*sign;  // 几个字的长度标志位就是 sign*n
        t = abs_ival;
        while (t) {
            *p++ = Py_SAFE_DOWNCAST(
                t & PyLong_MASK, unsigned long, digit);  // 循环写入低15位到到 ob_digit
            t >>= PyLong_SHIFT;  // 右移15位，消除写入的位数
        }
    }
    return (PyObject *)v;
}
```

- ```_PyLong_New(size)``` 创建 ```PyLongObject```

```c

/* Allocate a new int object with size digits.
   Return NULL and set exception if we run out of memory. */
// 为 size 大小的数字申请内存

#define MAX_LONG_DIGITS \
    ((PY_SSIZE_T_MAX - offsetof(PyLongObject, ob_digit))/sizeof(digit))

PyLongObject *_PyLong_New(Py_ssize_t size)
{
    PyLongObject *result;
    /* Number of bytes needed is: offsetof(PyLongObject, ob_digit) +
       sizeof(digit)*size.  Previous incarnations of this code used
       sizeof(PyVarObject) instead of the offsetof, but this risks being
       incorrect in the presence of padding between the PyVarObject header
       and the digits. */
// 需要的byte为 ： PyLongObject 的内存 + 数字的占的位数 * 数字的长度
    if (size > (Py_ssize_t)MAX_LONG_DIGITS) {  // 如果超出限制的话，则报错
        PyErr_SetString(PyExc_OverflowError,
                        "too many digits in integer");
        return NULL;
    }
    result = PyObject_MALLOC(offsetof(PyLongObject, ob_digit) +
                             size*sizeof(digit));
    if (!result) {
        PyErr_NoMemory();
        return NULL;
    }
    return (PyLongObject*)PyObject_INIT_VAR(result, &PyLong_Type, size);
}

```

#### PyVarObject 初始化

> python 中 int 类型的创建主要包含几个过程，即内存的申请、PyVarObject 初始化 和 内存的写入。在上面我们没有深入探究第二个步骤，下面我们来看一下具体的实现。

##### 内存申请

注意，申请的内存不仅包含了 PyLongObject 和 ob_digit 所占的内存，还包括了存储数字的内存

```c
 offsetof(PyLongObject, ob_digit) + sizeof(digit)*size
```

#### PyVarObject 初始化

> PyVarObject 

我们在 ```_PyObject_New``` 中看到过下面的代码。

```c
 return (PyLongObject*)PyObject_INIT_VAR(result, &PyLong_Type, size);

#define PyObject_INIT_VAR(op, typeobj, size) \
    _PyObject_INIT_VAR(_PyVarObject_CAST(op), (typeobj), (size))
```

先来看下 ```_PyObject_INIT_VAR``` 的定义

```c
static inline PyVarObject*
_PyObject_INIT_VAR(PyVarObject *op, PyTypeObject *typeobj, Py_ssize_t size)
{
    assert(op != NULL);
    Py_SIZE(op) = size;  // 这里即上面说的 op->ob_size = size
    PyObject_INIT((PyObject *)op, typeobj);
    return op;
}

#define PyObject_INIT(op, typeobj) \
    _PyObject_INIT(_PyObject_CAST(op), (typeobj))
```

下面我们来看```_PyObject_INIT```的具体的定义。

```c
/* Inline functions trading binary compatibility for speed:
   PyObject_INIT() is the fast version of PyObject_Init(), and
   PyObject_INIT_VAR() is the fast version of PyObject_InitVar.
   See also pymem.h.
   These inline functions expect non-NULL object pointers. */

static inline PyObject*
_PyObject_INIT(PyObject *op, PyTypeObject *typeobj)
{
    assert(op != NULL);
    Py_TYPE(op) = typeobj;  // 这里是 op->ob_type = typeobj，即将 op 的 type 复位 typeobj
    if (PyType_GetFlags(typeobj) & Py_TPFLAGS_HEAPTYPE) {  //当检查 这个 类型的 type 存在的时候,引用计数增加
        Py_INCREF(typeobj);    // 这里 typeobj->ob_refcnt++ ；总引用计数 +1
    }
    _Py_NewReference(op); // 这里是没有引用计数的时候，将当前 对象 的引用计数记为 1；op->ob_refcnt = 1
    return op;
}

```

##### 内存写入

内存的写入是根据数字转化为二进制的长度 size 决定的，具体的要看数字 size 的大小。




# 其他

> python 文档官方网址，包含了从 python 安装和使用的内容。

- [文档目录](https://docs.python.org/zh-cn/3/)
- [安装和使用 python](https://docs.python.org/zh-cn/3/using/index.html)
- [入门教程](https://docs.python.org/zh-cn/3/tutorial/index.html)
- [安装模块](https://docs.python.org/zh-cn/3/installing/index.html)
- [分发模块](https://docs.python.org/zh-cn/3/distributing/index.html)
- [常见问题](https://docs.python.org/zh-cn/3/faq/index.html)


## python 内置类型思维脑图 

> [文件原始链接](https://www.processon.com/view/link/5dbfd58ce4b0ea86c4204af9)

![](https://images.xiaozhuanlan.com/photo/2019/4ce73ee6be87112afe47602c7b0d1761.png)





