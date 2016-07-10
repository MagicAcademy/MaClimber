#!/usr/bin/env python
import http.cookiejar
import gzip
from urllib.request import Request
import sys,re
from urllib.request import quote
import urllib.parse as parse
from urllib.request import urlopen


class Spider(object):

    """
    爬虫母皇,含有抽象的公用方法
    """
    def __init__(self, url, config, max_depth=0):
        self.url = url
        self.config = config
        self.maxDepth = max_depth
        self.__currentDepth = 0
        self.__wholeList = []
        self.__filter = []
        self.__plugin = []
        self.singlePageMaxTrace = 10

    def getHtml(self):
        try:
            # 当要抓取的页面的地址不在 wholeList 中时,
            # 添加到 wholeList 中,并进行抓取
            # wholeList 是记录被抓取过的地址
            if self.url not in self.__wholeList:
                self.__wholeList.append(self.url)
            else:
                return

            # 当当前抓取深度 大于 预期抓取深度时
            if self.__currentDepth > self.maxDepth:
                return

            # 这个是分隔符?
            depthPrefix = ""
            for _ in range(self.__currentDepth):
                depthPrefix += "="
            depthPrefix += ">"

            # 拼接请求头部分
            req = Request(self.encode_uri())
            for item in config:
                req.add_header(item[0],item[1])

            # 发送请求头,并接收响应
            response = urlopen(req)

            # 获取响应头的属性
            http_message = response.info()
            contentType = http_message.get_content_type()
            if (contentType != "text/html") and (contentType != "text/plain"):
                log("%s %s | %s" % (depthPrefix,url,"Not HTML"))
                return

            # 字符编码
            serverCharset = http_message.get_content_charset()
            if serverCharset == None or serverCharset == "":
                serverCharset = "utf-8"

            html = response.read().decode(serverCharset)
            return html
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error with %s at line %s: %s" % (self.url, exc_tb.tb_lineno, e))

    def ungzip(self, data):
        try:
            print('unzip HTML...')
            data = gzip.decompress(data)
            print('finished')
        except:
            print('No need to be unzipped,pass...')
        return data

    def encode_uri(self):
        # 解析url
        result = parse.urlparse(self.url)

        # 将url的 path部分 以 / 切割,然后unicode编码,因为防止其中有中文
        path_tmp = result.path.split('/')
        for index in range(len(path_tmp)):
            path_tmp[index] = quote(path_tmp[index])

        # 将url 的 query部分 以 &切割
        query_tmp = result.query.split('&')
        for index in range(len(path_tmp)):
            if path_tmp[index] == "":
                continue
            path_parm_tmp = query_tmp[index].split("=")
            path_tmp[index] = quote(path_parm_tmp[0]) + quote(path_parm_tmp[1])

        return parse.urlunparse(
            (result.scheme, result.netloc, '/'.join(path_tmp), result.params, '&'.join(query_tmp), result.fragment)
        )


    def getLink(self,links):
        '''
        @SDD 纯爬虫方法 需要抽象
        :param maxcurrent_depth:
        :param whole_list:
        :return:
        '''
        try:
            # 这个是获取地址的 协议,是https协议还是http协议
            prot = ""
            if self.url.startswith("https"):
                prot = "https"
            else:
                prot = "http"

            # 这是获取网址的域名部分
            domain = ""
            d = re.findall("(http(?:s|):\/\/.+?)(?:[\/]|$)", self.url, re.DOTALL)
            domain = d[0]

            if len(links) < 1:
                log("%s No link found to trace" % ("=>"))
            else:
                list = []
                for x in links:
                    if x not in list:
                        list.append(x)
                    if self.singlePageMaxTrace != 0 and (len(list)) >= self.singlePageMaxTrace:
                        break
                self.__currentDepth += 1

                for item in list:
                    if item.startswith("http") or item.startswith("https"):
                        self.url = item
                        return self.getHtml()
                    elif item.startswith("//"):
                        self.url = "http:" + item
                        return self.getHtml()
                    elif item.startswith("#"):
                        pass
                    elif item.startswith("/"):
                        self.url = domain + item
                    elif item.startswith("javscript"):
                        pass
                    else:
                        self.url = domain + "/" + item
                        return self.getHtml()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error with %s at line %s: %s" % (self.url, exc_tb.tb_lineno, e))


    def getTitle(self, htmlcontent):
        m = re.findall('<title>(.+?)</title>', htmlcontent, re.DOTALL)
        if len(m) < 1:
            return "No title"
        else:
            return m[0]

    def setFilter(self,filter):
        self.__filter.append(filter)

    #  获取页面上的链接
    def filterRun(self,html):
        links = []

        # 筛选链接
        for filter in self.__filter:
            filter_result = filter(html)
            if type(filter_result) == "list" or type(filter_result) == "tupe":
                for link in filter_result:
                    links.append(link)
            else:
                links.append(filter_result)
        return links

    def setPlugins(self,plugin):
        self.__plugin.append(plugin)

    def pluginRun(self,html):
        for plugin in self.__plugin:
            plugin.run(html)

if __name__ == '__main__':
    config = [
        ("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
    ]
    s = Spider("http://www.bilibili.com/",config)
    s.getHtml()
    # print(s.getLink(["http://www.bilibili.com/","http://www.bilibili.com/video/douga.html"]))