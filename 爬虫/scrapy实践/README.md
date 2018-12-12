### 同时装有py2 和3,运行scrapy如何区分

>python2 -m scrapy startproject xxx

>python3 -m scrapy startproject xxx

当然，执行的时候也是

>python3 -m scrapy crawl spider

### MySql 执行 DELETE/UPDATE时，报 Error Code: 1175错误

MySql 执行 DELETE FROM Table 时，报 Error Code: 1175. You are using safe update mode and you tried to update a table without a WHERE that uses a KEY column To disable safe mode, toggle the option in Preferences -> SQL Editor and reconnect. 错误，这是因为 MySql 运行在 safe-updates模式下，该模式会导致非主键条件下无法执行update或者delete命令，执行命令如下命令

>SET SQL_SAFE_UPDATES = 0;

修改下数据库模式，然后就可以继续执行 DELETE/UPDATE 了
如果想改会 safe-updates模式，执行如下命令即可

>SET SQL_SAFE_UPDATES = 1;

## Scrapy

Scrapy 是用 Python 实现的一个为了爬取网站数据、提取结构性数据而编写的应用框架。

Scrapy 常应用在包括数据挖掘，信息处理或存储历史数据等一系列的程序中。

通常我们可以很简单的通过 Scrapy 框架实现一个爬虫，抓取指定网站的内容或图片。

制作 Scrapy 爬虫 一共需要4步：

* 新建项目 (scrapy startproject xxx)：新建一个新的爬虫项目
* 明确目标 （编写items.py）：明确你想要抓取的目标
* 制作爬虫 （spiders/xxspider.py）：制作爬虫开始爬取网页
* 存储内容 （pipelines.py）：设计管道存储爬取内容

项目中：

 * scrapy.cfg: 项目的配置文件。
 * scrapy框架/: 项目的Python模块，将会从这里引用代码。
 * job_com/items.py: 项目的目标文件。
 * job_com/pipelines.py: 项目的管道文件。
 * job_com/settings.py: 项目的设置文件。
 * job_com/spiders/: 存储爬虫代码目录。
 
 
### Request objects

> class scrapy.http.Request(url[, callback, method='GET', headers, body, cookies, meta, encoding='utf-8', priority=0, dont_filter=False, errback])

一个Request对象表示一个HTTP请求，它通常是在爬虫生成，并由下载执行，从而生成Response。

参数：

* url（string） - 此请求的网址
* callback（callable） - 将使用此请求的响应（一旦下载）作为其第一个参数调用的函数。有关更多信息，请参阅下面的将附加数据传递给回调函数。如果请求没有指定回调，parse()将使用spider的 方法。请注意，如果在处理期间引发异常，则会调用errback。
* method（string） - 此请求的HTTP方法。默认为'GET'。
* meta（dict） - 属性的初始值Request.meta。如果给定，在此参数中传递的dict将被浅复制。
* body（str或unicode） - 请求体。如果unicode传递了a，那么它被编码为 str使用传递的编码（默认为utf-8）。如果 body没有给出，则存储一个空字符串。不管这个参数的类型，存储的最终值将是一个str（不会是unicode或None）。
* headers（dict） - 这个请求的头。dict值可以是字符串（对于单值标头）或列表（对于多值标头）。如果 None作为值传递，则不会发送HTTP头。

cookie（dict或list） - 请求cookie。这些可以以两种形式发送。

使用dict：
```
request_with_cookies = Request(url="http://www.example.com",
                               cookies={'currency': 'USD', 'country': 'UY'})



    * 使用列表：


    request_with_cookies = Request(url="http://www.example.com",
                                   cookies=[{'name': 'currency',
                                            'value': 'USD',
                                            'domain': 'example.com',
                                         'path': '/currency'}])
   
```
后一种形式允许定制 cookie的属性domain和path属性。这只有在保存Cookie用于以后的请求时才有用。
当某些网站返回Cookie（在响应中）时，这些Cookie会存储在该域的Cookie中，并在将来的请求中再次发送。这是任何常规网络浏览器的典型行为。但是，如果由于某种原因，您想要避免与现有Cookie合并，您可以通过将dont_merge_cookies关键字设置为True 来指示Scrapy如此操作 Request.meta。
不合并Cookie的请求示例：
```
request_with_cookies = Request(url="http://www.example.com",
                               cookies={'currency': 'USD', 'country': 'UY'},
                               meta={'dont_merge_cookies': True})
```


* encoding（string） - 此请求的编码（默认为'utf-8'）。此编码将用于对URL进行百分比编码，并将正文转换为str（如果给定unicode）。
* priority（int） - 此请求的优先级（默认为0）。调度器使用优先级来定义用于处理请求的顺序。具有较高优先级值的请求将较早执行。允许负值以指示相对低优先级。
* dont_filter（boolean） - 表示此请求不应由调度程序过滤。当您想要多次执行相同的请求时忽略重复过滤器时使用。小心使用它，或者你会进入爬行循环。默认为False。
* errback（callable） - 如果在处理请求时引发任何异常，将调用的函数。这包括失败的404 HTTP错误等页面。它接收一个Twisted Failure实例作为第一个参数。有关更多信息，请参阅使用errbacks在请求处理中捕获异常。
* url包含此请求的网址的字符串。请记住，此属性包含转义的网址，因此它可能与构造函数中传递的网址不同。


meta
包含此请求的任意元数据的字典。此dict对于新请求为空，通常由不同的Scrapy组件（扩展程序，中间件等）填充。因此，此dict中包含的数据取决于您启用的扩展。

有关Scrapy识别的特殊元键列表，请参阅Request.meta特殊键。
当使用or 方法克隆请求时，此dict是浅复制的 ，并且也可以在您的爬虫中从属性访问。copy()replace()response.meta

copy（）
返回一个新的请求，它是这个请求的副本。另请参见： 将附加数据传递到回调函数。

replace([url, method, headers, body, cookies, meta, encoding, dont_filter, callback, errback])
返回具有相同成员的Request对象，但通过指定的任何关键字参数赋予新值的成员除外。该属性Request.meta是默认复制（除非新的值在给定的meta参数）。另请参见 将附加数据传递给回调函数。

将附加数据传递给回调函数

请求的回调是当下载该请求的响应时将被调用的函数。将使用下载的Response对象作为其第一个参数来调用回调函数。
例：
```
def parse_page1(self, response):
    return scrapy.Request("http://www.example.com/some_page.html",
                          callback=self.parse_page2)

def parse_page2(self, response):
    # this would log http://www.example.com/some_page.html
    self.logger.info("Visited %s", response.url)
```


在某些情况下，您可能有兴趣向这些回调函数传递参数，以便稍后在第二个回调中接收参数。您可以使用该Request.meta属性。
以下是使用此机制传递项目以填充来自不同页面的不同字段的示例：
```
def parse_page1(self, response):
    item = MyItem()
    item['main_url'] = response.url
    request = scrapy.Request("http://www.example.com/some_page.html",
                             callback=self.parse_page2)
    request.meta['item'] = item
    yield request

def parse_page2(self, response):
    item = response.meta['item']
    item['other_url'] = response.url
    yield item
```

使用errbacks在请求处理中捕获异常

请求的errback是在处理异常时被调用的函数。

它接收一个Twisted Failure实例作为第一个参数，并可用于跟踪连接建立超时，DNS错误等。

这里有一个示例爬虫记录所有错误，并捕获一些特定的错误，如果需要：
```
import scrapy

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class ErrbackSpider(scrapy.Spider):
    name = "errback_example"
    start_urls = [
        "http://www.httpbin.org/",              # HTTP 200 expected
        "http://www.httpbin.org/status/404",    # Not found error
        "http://www.httpbin.org/status/500",    # server issue
        "http://www.httpbin.org:12345/",        # non-responding host, timeout expected
        "http://www.httphttpbinbin.org/",       # DNS error expected
    ]

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse_httpbin,
                                    errback=self.errback_httpbin,
                                    dont_filter=True)

    def parse_httpbin(self, response):
        self.logger.info('Got successful response from {}'.format(response.url))
        # do something useful here...

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)


```

Request.meta特殊键

该Request.meta属性可以包含任何任意数据，但有一些特殊的键由Scrapy及其内置扩展识别。

那些是：
```

dont_redirect
dont_retry
handle_httpstatus_list
handle_httpstatus_all
dont_merge_cookies（参见cookies构造函数的Request参数）
cookiejar
dont_cache
redirect_urls
bindaddress
dont_obey_robotstxt
download_timeout
download_maxsize
download_latency
proxy
```
 bindaddress 用于执行请求的出站IP地址的IP。
 
download_timeout  下载器在超时前等待的时间量（以秒为单位）。

download_latency

自请求已启动以来，用于获取响应的时间量，即通过网络发送的HTTP消息。此元键仅在响应已下载时可用。虽然大多数其他元键用于控制Scrapy行为，但这应该是只读的。
请求子类;这里是内置子类的Request列表。您还可以将其子类化以实现您自己的自定义功能。

FormRequest对象

FormRequest类扩展了Request具有处理HTML表单的功能的基础。它使用lxml.html表单 从Response对象的表单数据预填充表单字段。
class scrapy.http.FormRequest(url[, formdata, ...])

本FormRequest类增加了新的构造函数的参数。其余的参数与Request类相同，这里没有记录。

参数：formdata（元组的dict或iterable） - 是一个包含HTML Form数据的字典（或（key，value）元组的迭代），它将被url编码并分配给请求的主体。
该FormRequest对象支持除标准以下类方法Request的方法：

classmethod from_response(response[, formname=None, formid=None, formnumber=0, formdata=None, formxpath=None, formcss=None, clickdata=None, dont_click=False, ...])

返回一个新FormRequest对象，其中的表单字段值已预先<form>填充在给定响应中包含的HTML 元素中。有关示例，请参阅 使用FormRequest.from_response（）来模拟用户登录。
该策略是在任何可查看的表单控件上默认自动模拟点击，如a 。即使这是相当方便，并且经常想要的行为，有时它可能导致难以调试的问题。例如，当使用使用javascript填充和/或提交的表单时，默认行为可能不是最合适的。要禁用此行为，您可以将参数设置 为。此外，如果要更改单击的控件（而不是禁用它），您还可以使用 参数。<input type="submit"> from_response() dont_click True clickdata
参数：

```

response（Responseobject） - 包含将用于预填充表单字段的HTML表单的响应
formname（string） - 如果给定，将使用name属性设置为此值的形式。
formid（string） - 如果给定，将使用id属性设置为此值的形式。
formxpath（string） - 如果给定，将使用匹配xpath的第一个表单。
formcss（string） - 如果给定，将使用匹配css选择器的第一个形式。
formnumber（integer） - 当响应包含多个表单时要使用的表单的数量。第一个（也是默认）是0。
formdata（dict） - 要在表单数据中覆盖的字段。如果响应<form>元素中已存在字段，则其值将被在此参数中传递的值覆盖。
clickdata（dict） - 查找控件被点击的属性。如果没有提供，表单数据将被提交，模拟第一个可点击元素的点击。除了html属性，控件可以通过其相对于表单中其他提交表输入的基于零的索引，通过nr属性来标识。
dont_click（boolean） - 如果为True，表单数据将在不点击任何元素的情况下提交。
```

这个类方法的其他参数直接传递给 FormRequest构造函数。

* 在新版本0.10.3：该formname参数。
*  在新版本0.17：该formxpath参数。
*  新的版本1.1.0：该formcss参数。
*  新的版本1.1.0：该formid参数。



请求使用示例

使用FormRequest通过HTTP POST发送数据

如果你想在你的爬虫中模拟HTML表单POST并发送几个键值字段，你可以返回一个FormRequest对象（从你的爬虫）像这样：
```
return [FormRequest(url="http://www.example.com/post/action",
                    formdata={'name': 'John Doe', 'age': '27'},
                    callback=self.after_post)]

```

使用FormRequest.from_response（）来模拟用户登录

网站通常通过元素（例如会话相关数据或认证令牌（用于登录页面））提供预填充的表单字段。
进行剪贴时，您需要自动预填充这些字段，并且只覆盖其中的一些，
例如用户名和密码。您可以使用 此作业的方法。这里有一个使用它的爬虫示例：

> <input type="hidden"> FormRequest.from_response()

```
import scrapy

class LoginSpider(scrapy.Spider):
    name = 'example.com'
    start_urls = ['http://www.example.com/users/login.php']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'john', 'password': 'secret'},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return

        # continue scraping with authenticated session...
```

响应对象

class scrapy.http.Response(url[, status=200, headers=None, body=b'', flags=None, request=None])
一个Response对象表示的HTTP响应，这通常是下载（由下载），并供给到爬虫进行处理。
参数：
```

url（string） - 此响应的URL
status（integer） - 响应的HTTP状态。默认为200。
headers（dict） - 这个响应的头。dict值可以是字符串（对于单值标头）或列表（对于多值标头）。
body（str） - 响应体。它必须是str，而不是unicode，除非你使用一个编码感知响应子类，如 TextResponse。
flags（list） - 是一个包含属性初始值的 Response.flags列表。如果给定，列表将被浅复制。
request（Requestobject） - 属性的初始值Response.request。这代表Request生成此响应。
```

* url

包含响应的URL的字符串。此属性为只读。更改响应使用的URL replace()。

status:表示响应的HTTP状态的整数。示例：200， 404。

* headers

包含响应标题的类字典对象。可以使用get()返回具有指定名称的第一个标头值或getlist()返回具有指定名称的所有标头值来访问值。例如，此调用会为您提供标题中的所有Cookie：
response.headers.getlist('Set-Cookie')

* body

本回复的正文。记住Response.body总是一个字节对象。如果你想unicode版本使用 TextResponse.text（只在TextResponse 和子类中可用）。
此属性为只读。更改响应使用的主体 replace()。

* request

Request生成此响应的对象。在响应和请求通过所有下载中间件后，此属性在Scrapy引擎中分配。特别地，这意味着：
HTTP重定向将导致将原始请求（重定向之前的URL）分配给重定向响应（重定向后具有最终URL）。

Response.request.url并不总是等于Response.url,此属性仅在爬虫程序代码和 Spider Middleware中可用，但不能在Downloader Middleware中使用（尽管您有通过其他方式可用的请求）和处理程序response_downloaded。

* meta

的快捷方式Request.meta的属性 Response.request对象（即self.request.meta）。
与Response.request属性不同，Response.meta 属性沿重定向和重试传播，因此您将获得Request.meta从您的爬虫发送的原始属性。
也可以看看equest.meta 属性

* flags

包含此响应的标志的列表。标志是用于标记响应的标签。例如：'cached'，'redirected '等等。
它们显示在Response（__ str__ 方法）的字符串表示上，它被引擎用于日志记录。

*  copy（）

返回一个新的响应，它是此响应的副本。

*  replace（[ url，status，headers，body，request，flags，cls ] ）

返回具有相同成员的Response对象，但通过指定的任何关键字参数赋予新值的成员除外。该属性Response.meta是默认复制。
urljoin（url ）

通过将响应url与可能的相对URL 组合构造绝对url。
这是一个包装在urlparse.urljoin，它只是一个别名，使这个调用：

>urlparse.urljoin(response.url, url)

响应子类

这里是可用的内置Response子类的列表。您还可以将Response类子类化以实现您自己的功能。

TextResponse对象

> class scrapy.http.TextResponse(url[, encoding[, ...]])

TextResponse对象向基Response类添加编码能力 ，这意味着仅用于二进制数据，例如图像，声音或任何媒体文件。

TextResponse对象支持一个新的构造函数参数，除了基础Response对象。其余的功能与Response类相同，这里没有记录。

参数：   encoding（string） - 是一个字符串，包含用于此响应的编码。如果你创建一个TextResponse具有unicode主体的对象，它将使用这个编码进行编码（记住body属性总是一个字符串）。如果encoding是None（默认值），则将在响应标头和正文中查找编码。
TextResponse除了标准对象之外，对象还支持以下属性Response

*  text

响应体，如unicode。
同样response.body.decode(response.encoding)，但结果是在第一次调用后缓存，因此您可以访问 response.text多次，无需额外的开销。

注意

unicode(response.body)不是一个正确的方法来将响应身体转换为unicode：您将使用系统默认编码（通常为ascii）而不是响应编码。

* encoding 包含此响应的编码的字符串。编码通过尝试以下机制按顺序解决：

在构造函数编码参数中传递的编码

在Content-Type HTTP头中声明的编码。如果此编码无效（即未知），则会被忽略，并尝试下一个解析机制。

在响应主体中声明的编码。TextResponse类不提供任何特殊功能。然而， HtmlResponse和XmlResponse类做。

通过查看响应体来推断的编码。这是更脆弱的方法，但也是最后一个尝试。

* selector

一个Selector使用响应为目标实例。选择器在第一次访问时被延迟实例化。

TextResponse对象除了标准对象外还支持以下方法Response：

* xpath（查询）

快捷方式TextResponse.selector.xpath(query)：

response.xpath('//p')

css(query)

快捷方式 TextResponse.selector.css(query):

response.css('p')

* body_as_unicode()

同样text，但可用作方法。保留此方法以实现向后兼容; 请喜欢response.text。

* HtmlResponse对象

class scrapy.http.HtmlResponse（url [，... ] ）

本HtmlResponse类的子类，TextResponse 这增加了通过查看HTML编码自动发现支持META HTTP-EQUIV属性。见TextResponse.encoding。

* XmlResponse对象

class scrapy.http.XmlResponse（url [，... ] ）

本XmlResponse类的子类，TextResponse这增加了通过查看XML声明线路编码自动发现支持。见TextResponse.encoding。




