

## requests

```
响应内容
我们能读取服务器响应的内容。再次以 GitHub 时间线为例：

>>> import requests
>>> r = requests.get('https://api.github.com/events')
>>> r.text
u'[{"repository":{"open_issues":0,"url":"https://github.com/...
Requests 会自动解码来自服务器的内容。大多数 unicode 字符集都能被无缝地解码。

请求发出后，Requests 会基于 HTTP 头部对响应的编码作出有根据的推测。当你访问 r.text 之时，Requests 会使用其推测的文本编码。
你可以找出 Requests 使用了什么编码，并且能够使用 r.encoding 属性来改变它：

>>> r.encoding
'utf-8'
>>> r.encoding = 'ISO-8859-1'
如果你改变了编码，每当你访问 r.text ，Request 都将会使用 r.encoding 的新值。你可能希望在使用特殊逻辑计算出文本的编码的情况下来修改编码。
比如 HTTP 和 XML 自身可以指定编码。这样的话，你应该使用 r.content 来找到编码，然后设置 r.encoding 为相应的编码。这样就能使用正确的编码解析 r.text 了。

在你需要的情况下，Requests 也可以使用定制的编码。如果你创建了自己的编码，并使用 codecs 模块进行注册，
你就可以轻松地使用这个解码器名称作为 r.encoding 的值， 然后由 Requests 来为你处理编码。

```


```
Requests 中也有一个内置的 JSON 解码器，助你处理 JSON 数据：

>>> import requests

>>> r = requests.get('https://api.github.com/events')
>>> r.json()

[{u'repository': {u'open_issues': 0, u'url': 'https://github.com/...
如果 JSON 解码失败， r.json() 就会抛出一个异常。例如，响应内容是 401 (Unauthorized)，尝试访问 r.json() 将会抛出 ValueError: No JSON object could be decoded 异常。

需要注意的是，成功调用 r.json() 并**不**意味着响应的成功。有的服务器会在失败的响应中包含一个 JSON 对象（比如 HTTP 500 的错误细节）。
这种 JSON 会被解码返回。要检查请求是否成功，请使用 r.raise_for_status() 或者检查 r.status_code 是否和你的期望相同。

```


```
原始响应内容
在罕见的情况下，你可能想获取来自服务器的原始套接字响应，那么你可以访问 r.raw。 如果你确实想这么干，那请你确保在初始请求中设置了 stream=True。具体你可以这么做：

>>> r = requests.get('https://api.github.com/events', stream=True)
>>> r.raw
<requests.packages.urllib3.response.HTTPResponse object at 0x101194810>
>>> r.raw.read(10)
'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03'
但一般情况下，你应该以下面的模式将文本流保存到文件：

with open(filename, 'wb') as fd:
    for chunk in r.iter_content(chunk_size):
        fd.write(chunk)
使用 Response.iter_content 将会处理大量你直接使用 Response.raw 不得不处理的。 当流下载时，上面是优先推荐的获取内容方式。 Note that chunk_size can be freely adjusted to a number that may better fit your use cases.


```

```

如果你想为请求添加 HTTP 头部，只要简单地传递一个 dict 给 headers 参数就可以了。

例如，在前一个示例中我们没有指定 content-type:

>>> url = 'https://api.github.com/some/endpoint'
>>> headers = {'user-agent': 'my-app/0.0.1'}

>>> r = requests.get(url, headers=headers)
注意: 定制 header 的优先级低于某些特定的信息源，例如：

如果在 .netrc 中设置了用户认证信息，使用 headers= 设置的授权就不会生效。而如果设置了 auth= 参数，``.netrc`` 的设置就无效了。
如果被重定向到别的主机，授权 header 就会被删除。
代理授权 header 会被 URL 中提供的代理身份覆盖掉。
在我们能判断内容长度的情况下，header 的 Content-Length 会被改写。
更进一步讲，Requests 不会基于定制 header 的具体情况改变自己的行为。只不过在最后的请求中，所有的 header 信息都会被传递进去。

注意: 所有的 header 值必须是 string、bytestring 或者 unicode。尽管传递 unicode header 也是允许的，但不建议这样做。

```

```

传递 URL 参数
你也许经常想为 URL 的查询字符串(query string)传递某种数据。如果你是手工构建 URL，那么数据会以键/值对的形式置于 URL 中，跟在一个问号的后面。例如， httpbin.org/get?key=val。 Requests 允许你使用 params 关键字参数，以一个字符串字典来提供这些参数。举例来说，如果你想传递 key1=value1 和 key2=value2 到 httpbin.org/get ，那么你可以使用如下代码：

>>> payload = {'key1': 'value1', 'key2': 'value2'}
>>> r = requests.get("http://httpbin.org/get", params=payload)
通过打印输出该 URL，你能看到 URL 已被正确编码：

>>> print(r.url)
http://httpbin.org/get?key2=value2&key1=value1
注意字典里值为 None 的键都不会被添加到 URL 的查询字符串里。

你还可以将一个列表作为值传入：

>>> payload = {'key1': 'value1', 'key2': ['value2', 'value3']}

>>> r = requests.get('http://httpbin.org/get', params=payload)
>>> print(r.url)
http://httpbin.org/get?key1=value1&key2=value2&key2=value3

```

```
二进制响应内容
你也能以字节的方式访问请求响应体，对于非文本请求：

>>> r.content
b'[{"repository":{"open_issues":0,"url":"https://github.com/...
Requests 会自动为你解码 gzip 和 deflate 传输编码的响应数据。

例如，以请求返回的二进制数据创建一张图片，你可以使用如下代码：

>>> from PIL import Image
>>> from io import BytesIO

>>> i = Image.open(BytesIO(r.content))
```
## re

```

模块定义了几个函数、 常量和异常。某些功能是充分的特色方法的已编译的正则表达式的简化的版本。大多数非平凡应用程序总是使用的已编译的形式。

re.compile(pattern, flags=0)
将正则表达式模式编译成一个正则表达式对象，它可以用于匹配使用它的match ()和search ()方法，如下所述。

可以通过指定flags值修改表达式的行为。值可以是任何以下变量，使用组合 OR （ |运算符）。

序列

prog = re.compile(pattern)
result = prog.match(string)
等效于

result = re.match(pattern, string)
但使用re.compile()和保存所产生的正则表达式对象重用效率更高时该表达式会在单个程序中多次使用。

注

 
传递给re.match()、 re.search()或re.compile()的最新模式的已编译的版本进行缓存，所以只有几个正则表达式的程序使用一次不必担心编译正则表达式。

re.DEBUG
显示调试信息编译的表达式。

re.I
re.IGNORECASE
执行不区分大小写的匹配 ；如[A-Z]表达式将太匹配小写字母。这不被受当前的区域设置。

re.L
re.LOCALE
Make \w, \W, \b, \B, \s and \S dependent on the current locale.

re.M
re.MULTILINE
当指定时，模式字符' ^'匹配字符串的开头以及每个行的开头（紧接每个换行符）； 模式字符'$'匹配字符串的末尾以及每一行的结尾（紧靠每个换行符之前）。默认情况下， '^'只匹配字符串的开始，'$'只匹配字符串的末尾和字符串末尾换行符（如果有的话）之前的位置。

re.S
re.DOTALL
使'.'特殊字符匹配任何字符，包括换行 ；如果没有此标志， '.'将匹配任何内容除换行符。

re.U
re.UNICODE
使得\w, \W, \b, \B, \d, \D, \s和 \S 取决于UNICODE定义的字符属性.

在 2.0 版中的新。

re.X
re.VERBOSE
此标志允许您编写正则表达式，看起来更好。在模式中的空白将被忽略，除非当在字符类或者前面非转义反斜杠，和，当一条线包含一个'#'既不在字符类中或由非转义反斜杠，从最左侧的所有字符之前，这种'#'通过行末尾将被忽略。

这意味着两个以下正则表达式匹配的对象，一个十进制数是相同的功能：

a = re.compile(r"""\d +  # the integral part
                   \.    # the decimal point
                   \d *  # some fractional digits""", re.X)
b = re.compile(r"\d+\.\d*")
re.search(pattern, string, flags=0)
扫描字符串，寻找的第一个由该正则表达式模式产生匹配的位置，并返回相应的MatchObject实例。返回None如果没有字符串中的位置匹配模式 ；请注意这不同于在字符串的某个位置中找到一个长度为零的匹配。

re.match(pattern, string, flags=0)
　　　如果在字符串的开头的零个或更多字符匹配正则表达式模式，将返回相应的MatchObject实例。返回None则该字符串中与模式不匹配；请注意这是不同于零长度匹配。

　　　请注意，即使在多行模式下， re.match()将只匹配字符串的开头，而不是在每个行的开头。

　　　如果你想要在字符串中的任意位置定位一个匹配，改用search () （请参见search () 与 match ()）。

re.fullmatch(pattern, string, flags=0)

如果整个字符串匹配正则表达式模式，则返回一个match对象。如果字符串与模式不匹配，则返回None；请注意：这与长度为0的match是有区别的。

新版本3.4

re.split(pattern, string, maxsplit=0, flags=0)
将字符串拆分的模式的匹配项。如果在模式中使用捕获括号，则然后也作为结果列表的一部分返回的文本模式中的所有组。如果maxsplit不为零，顶多maxsplit分裂发生，并且该字符串的其余部分将作为列表的最后一个元素返回。（不兼容性说明： 在原始的 Python 1.5 版本中， maxsplit被忽略。这已被固定在以后的版本。）

>>>
>>> re.split('\W+', 'Words, words, words.')
['Words', 'words', 'words', '']
>>> re.split('(\W+)', 'Words, words, words.')
['Words', ', ', 'words', ', ', 'words', '.', '']
>>> re.split('\W+', 'Words, words, words.', 1)
['Words', 'words, words.']
>>> re.split('[a-f]+', '0a3B9', flags=re.IGNORECASE)
['0', '3', '9']
如果在分离器有捕获组，它匹配字符串的开头，结果将启动与空字符串。同样对于字符串的末尾：

>>>
>>> re.split('(\W+)', '...words, words...')
['', '...', 'words', ', ', 'words', '...', '']
这样一来，分离器组件始终都位于相同的相对索引在结果列表中 （例如，如果有是在分离器，在 0，第二个捕获组等等）。

请注意，拆分将永远不会拆分对空模式匹配的字符串。举个例子：

>>>
>>> re.split('x*', 'foo')
['foo']
>>> re.split("(?m)^$", "foo\n\nbar\n")
['foo\n\nbar\n']
2.7 版本中的更改：添加可选的标志参数。

re.findall(pattern, string, flags=0)
作为一个字符串列表，在字符串中，返回所有非重叠匹配的模式。该字符串是从左到右扫描的，匹配按照发现的顺序返回。如果一个或多个组是本模式中，返回一个列表的群体 ；如果该模式具有多个组，这将是元组的列表。空匹配包含在结果中，除非他们接触到另一场匹配的开头。

在 1.5.2 版本新。

2.4 版本中的更改：添加可选的标志参数。

re.finditer(pattern, string, flags=0)
返回一个迭代器符合MatchObject情况 在 RE模式字符串中的所有非重叠的匹配。该字符串是扫描的左到右，和按发现的顺序返回匹配。空匹配包含在结果中，除非他们接触的另一个匹配的开头。

新版本 2.2 中的。

2.4 版本中的更改：添加可选的标志参数。

re.sub(pattern, repl, string, count=0, flags=0)
Return the string obtained by replacing the leftmost non-overlapping occurrences of pattern in string by the replacement repl. 如果pattern没有被找到， string不变。repl 可以是一个字符串或一个函数；如果是一个字符串, 任何反斜杠转义都会实现。那就是，\n会转化成一个换行符，\r 会转化成一个回车，等等。 未知的转义字符例如 \j不做处理。Backreferences, such as \6, are replaced with the substring matched by group 6 in the pattern. For example:

>>>
>>> re.sub(r'def\s+([a-zA-Z_][a-zA-Z_0-9]*)\s*\(\s*\):',
...        r'static PyObject*\npy_\1(void)\n{',
...        'def myfunc():')
'static PyObject*\npy_myfunc(void)\n{'
如果repl是一个函数，它被呼吁每个非重叠模式发生。该函数采用单个匹配对象作为参数，并返回替换字符串。举个例子：

>>>
>>> def dashrepl(matchobj):
...     if matchobj.group(0) == '-': return ' '
...     else: return '-'
>>> re.sub('-{1,2}', dashrepl, 'pro----gram-files')
'pro--gram files'
>>> re.sub(r'\sAND\s', ' & ', 'Baked Beans And Spam', flags=re.IGNORECASE)
'Baked Beans & Spam'
模式可以是一个字符串或重新对象。

可选参数计数是模式出现，要更换 ； 的最大次数计数必须为非负整数。如果省略或为零，所有事件将被替换。空匹配模式取代只有当不毗邻前一个匹配，所以子 ('x *' '-'， 'abc')返回'-a-b-c-'。

In string-type repl arguments, in addition to the character escapes and backreferences described above, \g<name> will use the substring matched by the group named name, as defined by the (?P<name>...) syntax. \g<number> uses the corresponding group number; \g<2> is therefore equivalent to \2, but isn’t ambiguous in a replacement such as \g<2>0. \20 would be interpreted as a reference to group 20, not a reference to group 2 followed by the literal character '0'. The backreference \g<0> substitutes in the entire substring matched by the RE.

2.7 版本中的更改：添加可选的标志参数。

re.subn(pattern, repl, string, count=0, flags=0)
执行相同的操作，如sub()，但返回一个元组（new_string， number_of_subs_made)。

2.7 版本中的更改：添加可选的标志参数。

re.escape(string)
返回的字符串与所有非字母数字带有反斜杠 ；这是有用的如果你想匹配一个任意的文本字符串，在它可能包含正则表达式元字符。

re.purge()
清除正则表达式缓存。

exception re.error
当一个字符串传递给这里的函数之一时引发的异常不是有效的正则表达式 （例如，它可能包含不匹配的括号） 或其他一些错误在编译或匹配过程中发生的时。如果一个字符串包含不匹配的一种模式，它永远不会是一个错误。

1.3. Regular Expression Objects
class re.RegexObject
编译的正则表达式对象支持以下方法和属性：

search(string[, pos[, endpos]])
扫描字符串寻找一个位置，在此正则表达式产生的匹配，并返回相应的作法实例。返回无如果没有字符串中的位置匹配模式 ；请注意这是不同于找到一个长度为零的匹配在一些点在字符串中。

可选的第二个参数pos给索引在字符串中搜索在哪里开始 ；它将默认为0。这并不完全等于切片的字符串 ； ' ^'模式字符匹配在真正开始的字符串和位置刚换行，但不是一定是在开始搜索的索引。

可选参数endpos限制了多远的字符串将被搜索 ；它将，如果字符串是endpos个字符长，因此，只有从pos到字符endpos - 1将搜索匹配项。如果endpos小于pos，没有比赛会发现，否则，如果rx是已编译的正则表达式对象， rx.search （字符串， 0， 50)相当于rx.search （字符串 [： 50]， 0)。

>>>
>>> pattern = re.compile("d")
>>> pattern.search("dog")     # Match at index 0
<_sre.SRE_Match object at ...>
>>> pattern.search("dog", 1)  # No match; search doesn't include the "d"
match(string[, pos[, endpos]])
　　如果在字符串的开头的零个或更多字符匹配这个正则表达式，将返回相应的作法实例。返回没有如果，则该字符串与模式不匹配请注意这是不同于零长度匹配。

　　可选pos和endpos参数具有相同的含义，至于search ()方法。

　　　>>>
　　　>>> pattern = re.compile("o")
　　　>>> pattern.match("dog")      # No match as "o" is not at the start of "dog".
　　　>>> pattern.match("dog", 1)   # Match as "o" is the 2nd character of "dog".
　　　<_sre.SRE_Match object at ...>
　　如果你想要在字符串中的任意位置找到一个匹配，改用search() （请参见search() 与 match()）。

fullmatch(string[, pos[, endpos]])
如果整个字符串匹配正则表达式模式，则返回一个match对象。如果字符串与模式不匹配，则返回None；请注意：这与长度为0的match是有区别的。

新版本3.4

>>> pattern = re.compile("o[gh]")
>>> pattern.fullmatch("dog")      # No match as "o" is not at the start of "dog".
>>> pattern.fullmatch("ogre")     # No match as not the full string matches.
>>> pattern.fullmatch("doggie", 1, 3)   # Matches within given limits.
<_sre.SRE_Match object; span=(1, 3), match='og'>
split(string, maxsplit=0)
与使用编译的模式的split ()函数相同。

findall(string[, pos[, endpos]])
类似于findall()的功能，使用编译的模式，但也接受可选的pos和endpos参数限制搜索区域像match()。

finditer(string[, pos[, endpos]])
类似于finditer()的功能，使用编译后的模式，但也接受可选的pos和endpos参数限制搜索区域像match()。

sub(repl, string, count=0)
使用编译的模式的sub()函数完全相同。

subn(repl, string, count=0)
使用编译的模式的subn()函数完全相同。

flags
正则表达式匹配的标志。这是给compile()和任何标志的组合(吗？...)模式中的内联标志。

groups
捕获模式中的组数。

groupindex
一本字典，由定义任何符号组名称映射(?P < id >)组号码。这本词典是空的如果在模式中使用了无符号的组。

pattern
模式字符串中从中重新对象的编译。

1.4. Match Objects
class re.MatchObject
Match 对象始终有一个为 True 的布尔值。因为 match() 和 search() 返回 None 如果不匹配的话，您可以测试是否符合简单 if 的语句：

match = re.search(pattern, string)
if match:
    process(match)
Match 对象支持下列方法和属性：

expand(template)
Return the string obtained by doing backslash substitution on the template string template, as done by the sub() method. Escapes such as\n are converted to the appropriate characters, and numeric backreferences (\1, \2) and named backreferences (\g<1>, \g<name>) are replaced by the contents of the corresponding group.

group([group1, ...])
返回Match对象的一个或多个子组。如果单个参数，结果是一个单一的字符串 ；如果有多个参数，其结果是参数每一项的元组。如果没有参数， group1默认为零 （整场比赛返回）。如果groupN参数为零，相应的返回值是整个匹配的字符串 ；如果它是在具有包容性的范围 [1..99]，它是模式进行相应的括号组匹配的字符串。如果组编号是负值或大于在模式中定义的组的数目，被引发IndexError异常。如果一组包含在模式不匹配的一部分中，相应的结果是没有。如果一组包含在模式匹配多次的一部分，则返回最后一场比赛。

>>>
>>> m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
>>> m.group(0)       # The entire match
'Isaac Newton'
>>> m.group(1)       # The first parenthesized subgroup.
'Isaac'
>>> m.group(2)       # The second parenthesized subgroup.
'Newton'
>>> m.group(1, 2)    # Multiple arguments give us a tuple.
('Isaac', 'Newton')
如果正则表达式使用（？P < 名称 >...) 语法， groupN参数也可能查明群体按他们的通讯组名称的字符串。如果字符串参数不用作模式中的组名称，被引发IndexError异常。

一个适度复杂的例子：

>>>
>>> m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
>>> m.group('first_name')
'Malcolm'
>>> m.group('last_name')
'Reynolds'
通过它们的索引还可以获取到已命名的组：

>>>
>>> m.group(1)
'Malcolm'
>>> m.group(2)
'Reynolds'
如果一组匹配多次，只有最后一个匹配可访问：

>>>
>>> m = re.match(r"(..)+", "a1b2c3")  # Matches 3 times.
>>> m.group(1)                        # Returns only the last match.
'c3'
groups([default])
返回包含所有匹配到的子组的元组， 从1到模式中的所有组。默认实参用于团体没有参加这场比赛 ；它将默认为None。（不兼容性说明： 在原始的 Python 1.5 版本中，如果元组是一个元素长，字符串将返回相反。在以后的版本 （从 1.5.1 对），单身人士返回元组在这种情况下)。

举个例子：

>>>
>>> m = re.match(r"(\d+)\.(\d+)", "24.1632")
>>> m.groups()
('24', '1632')
如果我们使小数点和一切在它以后可选，并不是所有的组可能会参加比赛。这些团体将默认为无，除非给出了默认参数：

>>>
>>> m = re.match(r"(\d+)\.?(\d+)?", "24")
>>> m.groups()      # Second group defaults to None.
('24', None)
>>> m.groups('0')   # Now, the second group defaults to '0'.
('24', '0')
groupdict([default])
返回一个包含所有的比赛，由子组名称键控的命名子群的字典。默认实参用于团体没有参加这场比赛 ；它将默认为None。举个例子：

>>>
>>> m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
>>> m.groupdict()
{'first_name': 'Malcolm', 'last_name': 'Reynolds'}
start([group])
end([group])
返回的开始和结束的由组； 匹配的子字符串的索引组的默认值为零 （即整个匹配的子字符串）。如果组存在，但却无助于这场比赛将返回-1 。对于一个匹配对象m和做贡献匹配的组g ，由组g （相当于m.group(g)） 匹配的子字符串是

m.string[m.start(g):m.end(g)]
请注意， m.start(group)将等于m.end(group) ，是否组匹配空字符串。例如后, m = re.search('b(c?)'， 'cba')、 m.start(0)是 1、 m.end(0)是 2， m.start(1)和m.end(1)是两个 2 和m.start(2)引发IndexError异常。

将删除的电子邮件地址remove_this的示例：

>>>
>>> email = "tony@tiremove_thisger.net"
>>> m = re.search("remove_this", email)
>>> email[:m.start()] + email[m.end():]
'tony@tiger.net'
span([group])
作法 m，对于返回 2 元组（m.start(group)， m.end(group))。请注意是否组不会助长这场比赛，这是（-1， -1）。组的默认值为零，整场比赛。

pos
Pos传递给下面的search ()或match ()方法的值。这是重新引擎开始寻找匹配的字符串中的索引。

endpos
Endpos传递给下面的search ()或match ()方法的值。这是之外，重新引擎不会将字符串中的索引。

lastindex
最后的整数索引匹配捕获组，或没有，如果没有组均在所有匹配。例如，表达式(a) b， ((a)(b))，并且（（ab））将有lastindex = = 1如果应用于字符串ab，同时表达(a)(b)将有lastindex = = 2，如果应用到相同的字符串。

lastgroup
最后一次的名称匹配捕获的组，或没有如果小组不是有一个名称，或者如果没有组均在所有匹配。

re
其match ()或search ()方法产生此作法实例的正则表达式对象。

string
Match ()或search ()传递的字符串。

1.5. Examples
1.5.1. 检查对子
在这个例子中，我们将使用下面的 helper 函数去更优雅地显示 match 对象：

def displaymatch(match):
    if match is None:
        return None
    return '<Match: %r, groups=%r>' % (match.group(), match.groups())
假设您要编写一个球员手为 5 个字符的字符串代表与代表一张卡，每个字符的扑克程序"a"ace、"k"为国王、 王后、 杰克的"j"、"t"为 10，"q"和"2"至"9"代表卡具有此值。

若想查看给定字符串是否为一手有效牌的话，可履行以下操作：

>>>
>>> valid = re.compile(r"^[a2-9tjqk]{5}$")
>>> displaymatch(valid.match("akt5q"))  # Valid.
"<Match: 'akt5q', groups=()>"
>>> displaymatch(valid.match("akt5e"))  # Invalid.
>>> displaymatch(valid.match("akt"))    # Invalid.
>>> displaymatch(valid.match("727ak"))  # Valid.
"<Match: '727ak', groups=()>"
That last hand, "727ak", contained a pair, or two of the same valued cards. 若想以正则表达式匹配它的话，可使用如下反向引用：

>>>
>>> pair = re.compile(r".*(.).*\1")
>>> displaymatch(pair.match("717ak"))     # Pair of 7s.
"<Match: '717', groups=('7',)>"
>>> displaymatch(pair.match("718ak"))     # No pairs.
>>> displaymatch(pair.match("354aa"))     # Pair of aces.
"<Match: '354aa', groups=('a',)>"
要找出对包括什么卡，一个可以以下列方式使用group的作法() 方法：

>>>
>>> pair.match("717ak").group(1)
'7'

# Error because re.match() returns None, which doesn't have a group() method:
>>> pair.match("718ak").group(1)
Traceback (most recent call last):
  File "<pyshell#23>", line 1, in <module>
    re.match(r".*(.).*\1", "718ak").group(1)
AttributeError: 'NoneType' object has no attribute 'group'

>>> pair.match("354aa").group(1)
'a'
1.5.2. 模拟 scanf() 函数
Python 目前没有相当于scanf()。正则表达式是一般功能更强大，但也更加冗长，比scanf()的格式字符串。下表提供了一些多或少scanf()格式标记和正则表达式之间的等价映射。

scanf() Token	Regular Expression
%c	.
%5c	.{5}
%d	[-+]?\d+
%e, %E, %f, %g	[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?
%i	[-+]?(0[xX][\dA-Fa-f]+|0[0-7]*|\d+)
%o	[-+]?[0-7]+
%s	\S+
%u	\d+
%x, %X	[-+]?(0[xX])?[\dA-Fa-f]+
若想从下述字符串提取文件名和数字

/usr/sbin/sendmail - 0 errors, 4 warnings
您将使用如下的 scanf() 格式

%s - %d errors, %d warnings
等价的正则表达式为

(\S+) - (\d+) errors, (\d+) warnings
1.5.3. search() vs. match()
Python 提供了两种不同的原始操作基于正则表达式： re.match()检查是否只在字符串的开头匹配而re.search()检查是否在任何地方 （这是默认情况下，Perl 做的） 的字符串匹配。

举个例子：

>>>
>>> re.match("c", "abcdef")  # No match
>>> re.search("c", "abcdef") # Match
<_sre.SRE_Match object at ...>
正则表达式开头' ^'可以用与search ()来限制进行匹配字符串的开头（“^”表示匹配字符串的开头）：

>>>
>>> re.match("c", "abcdef")  # No match
>>> re.search("^c", "abcdef") # No match
>>> re.search("^a", "abcdef")  # Match
<_sre.SRE_Match object at ...>
但是请注意在多行模式match ()只匹配字符串的开头而使用一个正则表达式开头的search () ' ^'将匹配每行开头。

>>>
>>> re.match('X', 'A\nB\nX', re.MULTILINE)  # No match
>>> re.search('^X', 'A\nB\nX', re.MULTILINE)  # Match
<_sre.SRE_Match object at ...>
1.5.4. 制作一个电话本
split ()将字符串拆分为传递模式由分隔的列表。该方法是将文本数据转换为数据结构，可以轻松地阅读和修改由 Python 作为显示在下面的示例创建一个电话簿非常宝贵。

首先，这里是输入。通常它可能来自一个文件，在这里我们使用的三重引号的字符串语法：

>>>
>>> text = """Ross McFluff: 834.345.1254 155 Elm Street
...
... Ronald Heathmore: 892.345.3428 436 Finley Avenue
... Frank Burger: 925.541.7625 662 South Dogwood Way
...
...
... Heather Albrecht: 548.326.4584 919 Park Place"""
由一个或多个换行符分隔条目。现在我们转换字符串到一个列表中的每个非空的行，有它自己的条目：

>>>
>>> entries = re.split("\n+", text)
>>> entries
['Ross McFluff: 834.345.1254 155 Elm Street',
'Ronald Heathmore: 892.345.3428 436 Finley Avenue',
'Frank Burger: 925.541.7625 662 South Dogwood Way',
'Heather Albrecht: 548.326.4584 919 Park Place']
最后，拆分到一个列表中的第一个名字、 姓氏、 电话号码和地址的每个条目。因为地址中有空格，我们劈裂的形态，在里面，我们使用maxsplit参数的split () ：

>>>
>>> [re.split(":? ", entry, 3) for entry in entries]
[['Ross', 'McFluff', '834.345.1254', '155 Elm Street'],
['Ronald', 'Heathmore', '892.345.3428', '436 Finley Avenue'],
['Frank', 'Burger', '925.541.7625', '662 South Dogwood Way'],
['Heather', 'Albrecht', '548.326.4584', '919 Park Place']]
：?模式匹配在冒号之后的最后一个名称，以便它不出现在结果列表中。与4 maxsplit ，我们可以分开的街道名称门牌号码：

>>>
>>> [re.split(":? ", entry, 4) for entry in entries]
[['Ross', 'McFluff', '834.345.1254', '155', 'Elm Street'],
['Ronald', 'Heathmore', '892.345.3428', '436', 'Finley Avenue'],
['Frank', 'Burger', '925.541.7625', '662', 'South Dogwood Way'],
['Heather', 'Albrecht', '548.326.4584', '919', 'Park Place']]
1.5.5. Text Munging
sub()替换字符串或函数的结果为每次出现的一种模式。此示例演示如何使用sub()具有功能"伪装"的文本，或随机中每个单词的句子除第一个和最后一个字符之外的所有字符的顺序：

>>>
>>> def repl(m):
...   inner_word = list(m.group(2))
...   random.shuffle(inner_word)
...   return m.group(1) + "".join(inner_word) + m.group(3)
>>> text = "Professor Abdolmalek, please report your absences promptly."
>>> re.sub(r"(\w)(\w+)(\w)", repl, text)
'Poefsrosr Aealmlobdk, pslaee reorpt your abnseces plmrptoy.'
>>> re.sub(r"(\w)(\w+)(\w)", repl, text)
'Pofsroser Aodlambelk, plasee reoprt yuor asnebces potlmrpy.'
1.5.6. 查找所有副词
search ()一样， findall()匹配所有出现的一种模式，而不仅仅是第一个。举个例子，如果你是一位作家，并且想要寻找一些文本中的副词所有，他或她可能会使用findall()以下列方式：

>>>
>>> text = "He was carefully disguised but captured quickly by police."
>>> re.findall(r"\w+ly", text)
['carefully', 'quickly']
1.5.7. 查找所有副词和它们的位置
如果你想比匹配的文本模式的所有匹配项有关详细信息， finditer()是有用的因为它提供的作法的实例，而不是字符串。继续前面的示例中，如果其中一个是一位想要找到所有的副词和他们的位置在一些文字作家，他或她会使用finditer()方式如下：

>>>
>>> text = "He was carefully disguised but captured quickly by police."
>>> for m in re.finditer(r"\w+ly", text):
...     print '%02d-%02d: %s' % (m.start(), m.end(), m.group(0))
07-16: carefully
40-47: quickly
1.5.8. Raw 字符串表示法
Raw string notation (r"text") keeps regular expressions sane. Without it, every backslash ('\') in a regular expression would have to be prefixed with another one to escape it. For example, the two following lines of code are functionally identical:

>>>
>>> re.match(r"\W(.)\1\W", " ff ")
<_sre.SRE_Match object at ...>
>>> re.match("\\W(.)\\1\\W", " ff ")
<_sre.SRE_Match object at ...>
当想要匹配文字反斜杠时，必须在正则表达式中先转义。With raw string notation, this means r"\\". Without raw string notation, one must use "\\\\", making the following lines of code functionally identical:

>>>
>>> re.match(r"\\", r"\\")
<_sre.SRE_Match object at ...>
>>> re.match("\\\\", r"\\")
<_sre.SRE_Match object at ...>

```

## findall

```

1. 先说一下findall()函数的两种表示形式
import re
kk = re.compile(r'\d+')
kk.findall('one1two2three3four4')
#[1,2,3,4]
 
#注意此处findall()的用法，可传两个参数;
kk = re.compile(r'\d+')
re.findall(kk,"one123")
#[1,2,3]
2. 正则表达式可能遇到的坑  --- 正则表达式中有括号()
1. 正则表达式中当没有括号时，就是正常匹配，在本例中"/w+/s+/w+"第一次匹配到的字符为"2345  3456",由于是贪婪模式会     继续匹配,第二次从"4567"开始匹配匹配到的结果为字符串"4567 5678"

 import re
string="2345  3456  4567  5678"
regex=re.compile("\w+\s+\w+")
print(regex.findall(string))
#['2345 3456', '4567 5678']
  !!!  首先的知道各个字符所表达的含义，这里只说一下/s 和 /S
       \s -- 匹配任何不可见字符，包括空格、制表符、换页符等等 
      \S -- 匹配任何可见字符   通常[/s/S] -- 可匹配任意字符
      [\s\S]*? -- 匹配懒惰模式的任意字符

2. 正则表达式中有一个括号时,其输出的内容就是括号匹配到的内容，而不是整个表达式所匹配到的结果,但是整个正则表达式执       行了只不过只输出括号匹配到的内容, 在第一次匹配时跟上述没有括号时一样，匹配到 "2345  3456" ,只不过只输出(/w+)匹配     到的结果 即"2345",第二次匹配同理从"4567" 开始，匹配到"4567  5678",但是还是只是输出"4567"

 import re
string="2345  3456  4567  5678"
regex=re.compile("(\w+)\s+\w+")
print(regex.findall(string))
#['2345', '4567']
3. 当正则表达式中有两个括号时，其输出是一个list 中包含2个 tuple,从输出的结果可以看出，有两个元组，每一个元组中有两       个字符串 : 其中第一个字符串"2345 3456"是最外面的括号输出的结果，第二个是里面括号(/w+)输出的结果 "2345", 第二个       元组是  第二次匹配的结果 -- 详解同第一次匹配。

import re
string="2345  3456  4567  5678"
regex=re.compile("((\w+)\s+\w+)")
print(regex.findall(string))
#[('2345  3456', '2345'), ('4567  5678', '4567')]


```

```

etree.HTML():构造了一个XPath解析对象并对HTML文本进行自动修正。

etree.tostring()：输出修正后的结果，类型是bytes

```

XPath 是一门在 XML 文档中查找信息的语言。XPath 可用来在 XML 文档中对元素和属性进行遍历。
XPath 是 W3C XSLT 标准的主要元素，并且 XQuery 和 XPointer 都构建于 XPath 表达之上


 fp.write("%s\t\t\t\t\t\t\t\t%s\n" % (s[0].encode("utf8"), s[1].encode("utf8")))
 
 二者之间增加空格