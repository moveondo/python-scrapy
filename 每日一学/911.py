#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def abs_my(x):
    if x>10:
        return "1jwejewhg"
    else:
        return "xiaoyu10"

print(abs_my(9))

def power(x):
    return x * x

print(power(9))

def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum

print(calc(10,1,2,3))

def fact(n):
    if n==1:
        return 1
    return n * fact(n - 1)

print(fact(3))

for x, y in [(1, 1), (2, 4), (3, 9)]:
   print(x, y)


d = {'x': 'A', 'y': 'B', 'z': 'C' }
#  for (k, v) in d.items():
#     print(k, '=', v)

L = ['Hello', 'World', 'IBM', 'Apple']
 print([s.lower() for s in L])