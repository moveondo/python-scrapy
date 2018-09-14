#!/usr/bin/env python3
# -*- coding: utf-8 -*-
n = 1
while n <= 100:
    if n > 10: # 当n = 11时，条件满足，执行break语句
        break # break语句会结束当前循环
    print(n)
    n = n + 1
print('END')

n = 0
while n < 10:
    n = n + 1
    if n % 2 == 0: # 如果n是偶数，执行continue语句
        continue # continue语句会直接继续下一轮循环，后续的print()语句不会执行
    print(n)

    
sum = 0
for x in range(101):
    sum = sum + x
print(sum)

sum=0
n=99
while n>0:
  sum=sum+n
  n=n-2
print(sum)

names = ['Michael', 'Bob', 'Tracy']
for name in names:
    print(name)


a = 100
if a >= 0:
    print(a);
else:
    print(-a);

a = 'ABC'
b = a
a = 'XYZ'
print(b)


n = 123
f = 456.789
s1 = 'Hello, world'
s2 = 'Hello, \'Adam\''
s3 = r'Hello, "Bart"'
s4 = r'''Hello,
Lisa!'''

# ss=len('中文'.encode('utf-8'))
# print(ss)

# age = 3
# if age >= 18:
#     print('adult')
# else:
#     print('teenager')



# s = input('birth: ')
# birth = int(s)
# if birth < 2000:
#     print('00前')
# else:
#     print('00后')
    