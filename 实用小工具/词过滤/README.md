

很短但是觉得挺有用的东东


USAGE:

    >>> f = DFAFilter()
    >>> f.add("操")
    >>> f.filter("我操")
       我*


知识点：

```
isinstance(object, classinfo)

参数
object -- 实例对象。

classinfo -- 可以是直接或间接类名、基本类型或者由它们组成的元组。

返回值

如果对象的类型与参数二的类型（classinfo）相同则返回 True，否则返回 False。。

对于基本类型来说 classinfo 可以是：

int，float，bool，complex，str(字符串)，list，dict(字典)，set，tuple

要注意的是，classinfo 的字符串是 str 而不是 string，字典也是简写 dict。

实例

arg=123
isinstance(arg, int)    #输出True
isinstance(arg, str)    #输出False
isinstance(arg, string) #报错

isinstance() 与 type() 区别：

type() 不会认为子类是一种父类类型，不考虑继承关系。

isinstance() 会认为子类是一种父类类型，考虑继承关系。

如果要判断两个类型是否相同推荐使用 isinstance()。

```


```
set() 函数创建一个无序不重复元素集，可进行关系测试，删除重复数据，还可以计算交集、差集、并集等。

>>>x = set('runoob')
>>> y = set('google')
>>> x, y

(set(['b', 'r', 'u', 'o', 'n']), set(['e', 'o', 'g', 'l']))   # 重复的被删除


```


```
collections是Python内建的一个集合模块，提供了许多有用的集合类。

defaultdict

使用dict时，如果引用的Key不存在，就会抛出KeyError。如果希望key不存在时，返回一个默认值，就可以用defaultdict：

>>> from collections import defaultdict
>>> dd = defaultdict(lambda: 'N/A')
>>> dd['key1'] = 'abc'
>>> dd['key1'] # key1存在
'abc'
>>> dd['key2'] # key2不存在，返回默认值
'N/A'
注意默认值是调用函数返回的，而函数在创建defaultdict对象时传入。

除了在Key不存在时返回默认值，defaultdict的其他行为跟dict是完全一样的。


deque
使用list存储数据时，按索引访问元素很快，但是插入和删除元素就很慢了，因为list是线性存储，数据量大的时候，插入和删除效率很低。

deque是为了高效实现插入和删除操作的双向列表，适合用于队列和栈：

>>> from collections import deque
>>> q = deque(['a', 'b', 'c'])
>>> q.append('x')
>>> q.appendleft('y')
>>> q
deque(['y', 'a', 'b', 'c', 'x'])
deque除了实现list的append()和pop()外，还支持appendleft()和popleft()，这样就可以非常高效地往头部添加或删除元素。



```

```
python assert断言的作用

python assert断言是声明其布尔值必须为真的判定，如果发生异常就说明表达示为假。可以理解assert断言语句为raise-if-not，用来测试表示式，其返回值为假，就会触发异常。

```