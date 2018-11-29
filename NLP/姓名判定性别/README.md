

Gender
根据中文姓名猜测其性别

 * 不到20行纯Python代码(核心部分)

 * 无任何依赖库

 * 兼容python3, python2, pypy

 * 82%的准确率

 * 可用于猜测性别

 * 也可用于判断名字的男性化/女性化程度





原理

 * 数学贝叶斯公式: P(Y|X) = P(X|Y) * P(Y) / P(X)

 * 当X条件独立时, P(X|Y) = P(X1|Y) * P(X2|Y) * ...

应用到猜名字上

```
P(gender=男|name=本山) 

= P(name=本山|gender=男) * P(gender=男) / P(name=本山)

= P(name has 本|gender=男) * P(name has 山|gender=男) * P(gender=男) / P(name=本山)

```

计算

 * 文件charfreq.csv是怎么来的?

   >曾经有个东西叫开房记录.avi(雾)，里面有名字和性别, 2000w条, 统计一下得出

 * 怎么算 P(name has 本|gender=男)?

   >“本”在男性名字中出现的次数 / 男性字出现的总次数

 * 怎么算 P(gender=男)?

   >男性名出现的次数 / 总次数

 * 怎么算 P(name=本山)?

   >不用算, 在算概率的时候会互相约去

### 坑

```
>>> ngender.guess('李胜男')
('male', 0.851334658742)
虽然两个字都很偏男性，但是结合起来就是女性名
```


```

1. * pm / (pm + pf)

先把分子转化为浮点型



python assert断言是声明其布尔值必须为真的判定，如果发生异常就说明表达示为假。
可以理解assert断言语句为raise-if-not，用来测试表示式，其返回值为假，就会触发异常

```


```
Python 字典(Dictionary) get() 函数返回指定键的值，如果值不在字典中返回默认值。

语法
get()方法语法：

dict.get(key, default=None)
参数
key -- 字典中要查找的键。
default -- 如果指定键的值不存在时，返回该默认值值。
返回值
返回指定键的值，如果值不在字典中返回默认值None。

实例
以下实例展示了 get()函数的使用方法：

#!/usr/bin/python

dict = {'Name': 'Zara', 'Age': 27}

print "Value : %s" %  dict.get('Age')
print "Value : %s" %  dict.get('Sex', "Never")
以上实例输出结果为：

Value : 27
Value : Never
```