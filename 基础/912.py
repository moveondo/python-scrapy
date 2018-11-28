#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def r(x):
    return x*x;

f=map(r,[1,2,3,4]);
print(list(f));


L = []
for n in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
    L.append(r(n))
print(L)

def is_odd(x):
    return x%2==0

print(filter(is_odd,[1,2,3,4,5,6,7,8,9]))

def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n

def _not_divisible(n):
    return lambda x: x % n > 0

def primes():
    yield 2
    it = _odd_iter() # 初始序列
    while True:
        n = next(it) # 返回序列的第一个数
        yield n
        it = filter(_not_divisible(n), it) # 构造新序列

# for n in primes():
#     if n < 1000:
#         print(n)
#     else:
#         break


def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs

f1, f2, f3 = count();

print(f1())
# print(f2())
# print(f3())


#  args = (10, 5, 6, 7)
#  print(max(*args))

# list(map(lambda x: x * x, [1, 2, 3, 4, 5, 6, 7, 8, 9]))

#lambda

# def how():
#     print("12345")

#  num=how
#  print(num())

#  def log1(func):
#     def wrapper(*args, **kw):
#         print('call %s():' % func.__name__)
#         return func(*args, **kw)
#     return wrapper

#     @log1
# def now():
#     print('2015-3-25')

 