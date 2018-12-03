

### python configparser模块
ConfigParser模块在python中用来读取配置文件，配置文件的格式跟windows下的ini配置文件相似，可以包含一个或多个节(section), 每个节可以有多个参数（键=值）。使用的配置文件的好处就是不用在程序员写死，可以使程序更灵活。 

注意：在python 3 中ConfigParser模块名已更名为configparser

configparser函数常用方法：

读取配置文件：

```
 1 read(filename) #读取配置文件，直接读取ini文件内容
 2 
 3 sections() #获取ini文件内所有的section，以列表形式返回['logging', 'mysql']
 4 
 5 options(sections) #获取指定sections下所有options ，以列表形式返回['host', 'port', 'user', 'password']
 6 
 7 items(sections) #获取指定section下所有的键值对，[('host', '127.0.0.1'), ('port', '3306'), ('user', 'root'), ('password', '123456')]
 8 
 9 get(section, option) #获取section中option的值，返回为string类型
10 >>>>>获取指定的section下的option <class 'str'> 127.0.0.1
11 
12 getint(section,option) 返回int类型
13 getfloat(section, option)  返回float类型
14 getboolean(section,option) 返回boolen类型

```
举例如下：
```
配置文件ini如下：


[logging]
level = 20
path =
server =

[mysql]
host=127.0.0.1
port=3306
user=root
password=123456

```


注意，也可以使用：替换=

代码如下：

```
import configparser
from until.file_system import get_init_path

conf = configparser.ConfigParser()
file_path = get_init_path()
print('file_path :',file_path)
conf.read(file_path)

sections = conf.sections()
print('获取配置文件所有的section', sections)

options = conf.options('mysql')
print('获取指定section下所有option', options)


items = conf.items('mysql')
print('获取指定section下所有的键值对', items)


value = conf.get('mysql', 'host')
print('获取指定的section下的option', type(value), value)

运行结果如下：


file_path : /Users/xxx/Desktop/xxx/xxx/xxx.ini
获取配置文件所有的section ['logging', 'mysql']
获取指定section下所有option ['host', 'port', 'user', 'password']
获取指定section下所有的键值对 [('host', '127.0.0.1'), ('port', '3306'), ('user', 'root'), ('password', '123456')]
获取指定的section下的option <class 'str'> 127.0.0.1
复制代码
 
```


### dict

Python内置了字典：dict的支持，dict全称dictionary，在其他语言中也称为map，使用键-值（key-value）存储，具有极快的查找速度。

举个例子，假设要根据同学的名字查找对应的成绩，如果用list实现，需要两个list：

```
names = ['Michael', 'Bob', 'Tracy']

scores = [95, 75, 85]

```

给定一个名字，要查找对应的成绩，就先要在names中找到对应的位置，再从scores取出对应的成绩，list越长，耗时越长。

如果用dict实现，只需要一个“名字”-“成绩”的对照表，直接根据名字查找成绩，无论这个表有多大，查找速度都不会变慢。用Python写一个dict如下：

```
>>> d = {'Michael':95, 'Bob':75, 'Tracy':85}

>>> d['Michael']

95

```

为什么dict查找速度这么快？因为dict的实现原理和查字典是一样的。假设字典包含了1万个汉字，我们要查某一个字，一个办法是把字典从第一页往后翻，直到找到我们想要的字为止，这种方法就是在list中查找元素的方法，list越大，查找越慢。

第二种方法是先在字典的索引表里（比如部首表）查这个字对应的页码，然后直接翻到该页，找到这个字。无论找哪个字，这种查找速度都非常快，不会随着字典大小的增加而变慢。

dict就是第二种实现方式，给定一个名字，比如'Michael'，dict在内部就可以直接计算出Michael对应的存放成绩的“页码”，也就是95这个数字存放的内存地址，直接取出来，所以速度非常快。


### 使用 pprint 模块

pprint 模块( pretty printer )

用于打印 Python 数据结构. 当你在命令行下打印特定数据结构时你会发现它很有用(输出格式比较整齐, 便于阅读).


在进行接口测试的时候，我们会调用多个接口发出多个请求，在这些请求中有时候需要保持一些共用的数据，例如cookies信息。

1、requests库的session对象能够帮我们跨请求保持某些参数，也会在同一个session实例发出的所有请求之间保持cookies。

s = requests.session()
#### req_param = '{"belongId": "300001312","userName": "alitestss003","password":"pxkj88","captcha":"pxpx","captchaKey":"59675w1v8kdbpxv"}'
#### res = s.post('http://test.e.fanxiaojian.cn/metis-in-web/auth/login', json=json.loads(req_param))
#### res1 = s.get("http://test.e.fanxiaojian.cn/eos--web/analysis/briefing")
#### print(res.cookies.values())   获取登陆的所有session


2、requests库的session对象还能为我们提供请求方法的缺省数据，通过设置session对象的属性来实现
eg:
#### 创建一个session对象  

s = requests.Session()  

#### 设置session对象的auth属性，用来作为请求的默认参数  

s.auth = ('user', 'pass')  

#### 设置session的headers属性，通过update方法，将其余请求方法中的headers属性合并起来作为最终的请求方法的headers  

s.headers.update({'x-test': 'true'})  

#### 发送请求，这里没有设置auth会默认使用session对象的auth属性，这里的headers属性会与session对象的headers属性合并  

r = s.get('http://httpbin.org/headers', headers={'x-test2': 'true'})  

上面的请求数据等于：{'Authorization': 'Basic dXNlcjpwYXNz', 'x-test': 'false'}

#### 查看发送请求的请求头  

```
r.request.headers      #打印响应中请求的所有header数据

res3 = s.get("http://pre.n.cn/irs-web/sso/login",cookies = cookie)
print(res3.request.headers.get("Cookie").split("IRSSID=")[-1])
print(type(res3.request.headers.get("Cookie").split("IRSSID=")[-1]))
print(res3.request._cookies)
```



不深思则不能造于道。不深思而得者，其得易失。



