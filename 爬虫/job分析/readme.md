### Python pass 语句

Python pass是空语句，是为了保持程序结构的完整性。

pass 不做任何事情，一般用做占位语句。
```
def sample(n_samples):	# Generate random samples from the fitted Gaussian distribution.

    pass
		
```

在python中有时候能看到定义一个def函数，函数内容部分填写为pass。

这里的pass主要作用就是占据位置，让代码整体完整。如果定义一个函数里面为空，

那么就会报错，当你还没想清楚函数内部内容，就可以用pass来进行填坑。


### Error：IndexError: list index out of range

Where?

　　对Python中有序序列进行按索引取值的时候，出现这个异常

Why?

　　对于有序序列： 字符串 str 、列表 list 、元组 tuple进行按索引取值的时候，默认范围为 0 ~ len(有序序列)-1，计数从0开始，而不是从1开始，最后一位索引则为总长度减去1。当然也可以使用 负数表示从倒数第几个，计数从-1开始，则对于有序序列，总体范围为 -len(有序序列) ~ len(有序序列)-1，如果输入的取值结果不在这个范围内，则报这个错

Way?

　　检查索引是否在 -len(有序序列) ~ len(有序序列)-1 范围内，修改正确

错误代码：

```
name = "beimenchuixue"
students = ["beimenchuixue", "boKeYuan", "Python", "Golang"]
print(name[20])
print(students[4])
```

正确代码：

```
name = "beimenchuixue"
students = ["beimenchuixue", "boKeYuan", "Python", "Golang"]
print(name[3])
print(students[3])
```
##Beautiful Soup

   提供一些简单的、python式的函数用来处理导航、搜索、修改分析树等功能。它是一个工具箱，通过解析文档为用户提供需要抓取的数据，因为简单，所以不需要多少代码就可以写出一个完整的应用程序。

　　Beautiful Soup自动将输入文档转换为Unicode编码，输出文档转换为utf-8编码。你不需要考虑编码方式，除非文档没有指定一个编码方式，这时，Beautiful Soup就不能自动识别编码方式了。然后，你仅仅需要说明一下原始编码方式就可以了。

　　Beautiful Soup已成为和lxml、html6lib一样出色的python解释器，为用户灵活地提供不同的解析策略或强劲的速度。


### yield

python中有一个非常有用的语法叫做生成器，所利用到的关键字就是yield。有效利用生成器这个工具可以有效地节约系统资源，避免不必要的内存占用。

一段代码
```
def fun():
for i in range(20):
    x=yield i
    print('good',x)

if __name__ == '__main__':
a=fun()
a.__next__()
x=a.send(5)
print(x)
```
这段代码很短，但是诠释了yield关键字的核心用法，即逐个生成。在这里获取了两个生成器产生的值，即0和1。分别由next函数和send()函数获得，这两个函数的区别我们后面会详细阐述。
关于__next__函数，这里先说明一下，我们可以利用__next__()这个函数持续获取符合fun函数规则的数，直到19结束。这段代码如下所示：

```
def fun():
for i in range(20):
    x=yield i

if __name__ == '__main__':
for x in fun():
    print(x)
```
这段代码的效果和下面这段代码是完全相同的

```

if __name__ == '__main__':
for i in range(20):
    x=yield i
```
for..in调用生成器算是生成器的基础用法，不过只会用for..in意义是不大的。生成器中最重要的函数是sent和__next__这两个函数，下面就针对这两个函数进行详细的阐述。

sent函数
这里特别强调了sent函数，因为sent函数没有那么直观。__next__函数很好理解，就是从上一个终止点开始，到下一个yield结束，返回值就是yield表达式的值。
例如在初始的那段代码里：

```
def fun():
for i in range(20):
    x=yield i
    print('good',x)
```

第一次调用__next__函数的时候，我们从fun的起点开始，然后在yield处结束，需要注意的是，赋值语句不会调用，此处yield i和含义和return差不多。
但是第二次调用__next__函数的时候，就会直接从上一个yield的结束处开始，也就是先执行赋值语句，然后输出字符串，进入下一个循环，直到下一个yield或者生成器结束
再次看初始的那段代码，可以发现第二次调用的时候没有选择使用__next__函数，而是使用了一个sent()函数。这里就需要注意，sent()函数的用法和__next__函数不太一样。sent()函数只能从yield之后开始，到下一个yield结束。这也就意味着第一次调用必须使用__next__函数。
sent()函数最重要的作用在于它可以给yield对应的赋值语句赋值，比如上面那一段代码中的

> x=yield i

如果调用__next()__函数，那么x=None。但是如果调用sent(5)，那么x=5。除了上述将的两个特征以外，sent和next并没有什么区别，sent函数也会返回yield表达式对应的值

next函数调用次可能有限
需要特别注意的是，尽管是生成器。但是next函数的调用次数可能是有限的。比如下面这段代码

```
def fun():
for i in range(20):
    x=yield i
    print('good',x)

if __name__ == '__main__':
a=fun()
for i in range(30):
    x=a.__next__()
    print(x)
    
```
生成器里的函数只循环了20次，但是next函数却调用了30次，这时候就会触发StopIteration异常。


