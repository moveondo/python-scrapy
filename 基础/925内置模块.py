# -*- coding: utf-8 -*-

#coding=utf-8

from datetime import datetime
now = datetime.now() 
print(now)

dt = datetime(2015, 4, 19, 12, 20) # 用指定日期时间创建datetime
print(dt)

cday = datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
print(cday)


# utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
# print(utc_dt)


# bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
# print(bj_dt)


from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print(p.x)

print(isinstance(p, Point))

Circle = namedtuple('Circle', ['x', 'y', 'r'])

from collections import OrderedDict
#od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])

od = OrderedDict()
od['z'] = 1
od['y'] = 2
od['x'] = 3

print(list(od.keys()))

from collections import Counter
c = Counter()
for ch in 'programming':
    c[ch] = c[ch] + 1
print(c)


import struct
print(struct.pack('>I', 10240099))


import hashlib

md5 = hashlib.md5()
md5.update('how to use md5 in '.encode('utf-8'))
md5.update('python hashlib?'.encode('utf-8'))
print(md5.hexdigest())


import itertools
natuals = itertools.count(1)
# for n in natuals:
#   print(n)

ns = itertools.repeat('ABC', 3)
for n in ns:
    print(n)


for c in itertools.chain('ABC', 'XYZ'):
    print(c)