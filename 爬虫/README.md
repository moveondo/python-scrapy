## 1. 对于反爬虫机制的处理
1.1 使用代理

适用情况：限制IP地址情况，也可解决由于“频繁点击”而需要输入验证码登陆的情况。

这种情况最好的办法就是维护一个代理IP池，网上有很多免费的代理IP，良莠不齐，可以通过筛选找到能用的。对于“频繁点击”的情况，我们还可以通过限制爬虫访问网站的频率来避免被网站禁掉。
```
proxies = {'http':'http://XX.XX.XX.XX:XXXX'}
Requests：
	import requests
	response = requests.get(url=url, proxies=proxies)
Urllib2：
	import urllib2
	proxy_support = urllib2.ProxyHandler(proxies)
	opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
	urllib2.install_opener(opener) # 安装opener，此后调用urlopen()时都会使用安装过的opener对象
	response = urllib2.urlopen(url)

```

1.2 时间设置

适用情况：限制频率情况。

```
Requests，Urllib2都可以使用time库的sleep()函数：

import time
time.sleep(1)
```

1.3 伪装成浏览器，或者反“反盗链”

有些网站会检查你是不是真的浏览器访问，还是机器自动访问的。这种情况，加上User-Agent，表明你是浏览器访问即可。有时还会检查是否带Referer信息还会检查你的Referer是否合法，一般再加上Referer。
```
headers = {'User-Agent':'XXXXX'} # 伪装成浏览器访问，适用于拒绝爬虫的网站
headers = {'Referer':'XXXXX'}
headers = {'User-Agent':'XXXXX', 'Referer':'XXXXX'}
Requests：
	response = requests.get(url=url, headers=headers)
Urllib2：
	import urllib, urllib2   
	req = urllib2.Request(url=url, headers=headers)
	response = urllib2.urlopen(req)
```

## 2. 对于断线重连

不多说。
```
def multi_session(session, *arg):
	retryTimes = 20
	while retryTimes>0:
		try:
			return session.post(*arg)
		except:
			print '.',
			retryTimes -= 1
```

或者

```
def multi_open(opener, *arg):
	retryTimes = 20
	while retryTimes>0:
		try:
			return opener.open(*arg)
		except:
			print '.',
			retryTimes -= 1
			
```
这样我们就可以使用multi_session或multi_open对爬虫抓取的session或opener进行保持。

## 3. 对于Ajax请求的处理


对于“加载更多”情况，使用Ajax来传输很多数据。

它的工作原理是：从网页的url加载网页的源代码之后，会在浏览器里执行JavaScript程序。这些程序会加载更多的内容，“填充”到网页里。这就是为什么如果你直接去爬网页本身的url，你会找不到页面的实际内容。

这里，若使用Google Chrome分析”请求“对应的链接(方法：右键→审查元素→Network→清空，点击”加载更多“，出现对应的GET链接寻找Type为text/html的，点击，查看get参数或者复制Request URL)，循环过程。

如果“请求”之前有页面，依据上一步的网址进行分析推导第1页。以此类推，抓取抓Ajax地址的数据。
对返回的json格式数据(str)进行正则匹配。json格式数据中，需从'\uxxxx'形式的unicode_escape编码转换成u'\uxxxx'的unicode编码。


## 4. 自动化测试工具Selenium

Selenium是一款自动化测试工具。它能实现操纵浏览器，包括字符填充、鼠标点击、获取元素、页面切换等一系列操作。总之，凡是浏览器能做的事，Selenium都能够做到。

这里列出在给定城市列表后，使用selenium来动态抓取去哪儿网的票价信息的代码。

##8. 验证码识别

对于网站有验证码的情况，我们有三种办法：

>使用代理，更新IP。

>使用cookie登陆。

>验证码识别。

使用代理和使用cookie登陆之前已经讲过，下面讲一下验证码识别。

可以利用开源的Tesseract-OCR系统进行验证码图片的下载及识别，将识别的字符传到爬虫系统进行模拟登陆。当然也可以将验证码图片上传到打码平台上进行识别。如果不成功，可以再次更新验证码识别，直到成功为止。

Robots协议
好的网络爬虫，首先需要遵守Robots协议。Robots协议（也称为爬虫协议、机器人协议等）的全称是“网络爬虫排除标准”（Robots Exclusion Protocol），网站通过Robots协议告诉搜索引擎哪些页面可以抓取，哪些页面不能抓取。

在网站根目录下放一个robots.txt文本文件（如 https://www.taobao.com/robots.txt ），里面可以指定不同的网络爬虫能访问的页面和禁止访问的页面，指定的页面由正则表达式表示。网络爬虫在采集这个网站之前，首先获取到这个robots.txt文本文件，然后解析到其中的规则，然后根据规则来采集网站的数据。

## 9. Robots协议规则

>User-agent: 指定对哪些爬虫生效

>Disallow: 指定不允许访问的网址

>Allow: 指定允许访问的网址

>注意: 一个英文要大写，冒号是英文状态下，冒号后面有一个空格，"/"代表整个网站

2. Robots协议举例

```
禁止所有机器人访问
	User-agent: *
	Disallow: /
允许所有机器人访问
	User-agent: *
	Disallow: 
禁止特定机器人访问
	User-agent: BadBot
	Disallow: /
允许特定机器人访问
	User-agent: GoodBot
	Disallow: 
禁止访问特定目录
	User-agent: *
	Disallow: /images/
仅允许访问特定目录
	User-agent: *
	Allow: /images/
	Disallow: /
禁止访问特定文件
	User-agent: *
	Disallow: /*.html$
仅允许访问特定文件
	User-agent: *
	Allow: /*.html$
	Disallow: /
	
```

> sudo -H pip install Scrapy

