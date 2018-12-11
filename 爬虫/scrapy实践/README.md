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



