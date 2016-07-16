# MaClimber :mountain_cableway:
我们想做一个通用的爬虫脚本,~~能屈能伸~~功能弹性化.

### 环境与依赖
* python>=3.4
* mysql>=5.2
* [SQLAlchemy](http://www.sqlalchemy.org/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

### 文件夹结构
```bash
+-core //核心功能
|   |-cache.py //缓存
|   |-connection.py //数据库连接
|   |-spider.py //爬虫母皇
+-migration //sql文件
|   |-your.sql
+-run //实际运行入库
    |-example.py
    
```
### 运行