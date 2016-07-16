#!/usr/bin/env python
import http.cookiejar
import gzip
from urllib.request import Request
import sys,re
from urllib.request import quote
import urllib.parse as parse
from urllib.request import urlopen


class Spider(object):

    def __init__ (self,maxDepth = 10,singlePageMaxTrace = 10):
        self.__wholeList = []
        self.__filters = []
        self.__plugins = []
        self.__maxDepth = maxDepth
        self.__singlePageMaxTrace = singlePageMaxTrace
        self.__url = ""
        self.__config = []
        self.__currentDepth = 0
        self.__domain = ""
        self.__prot = ""

    def setFilters (self,filter):
        self.__filters.append(filter)

    def setPlugin (self,plugin):
        self.__plugins.append(plugin)

    def setConfig (self,config):
        self.__config = config

    # 获取http地址
    def filtersRun (self,html):
        urls = []
        for filter in self.__filters:
            urls.extend(filter(html))
        return urls

    # 将获取的html内容提供给plugin使用
    def pluginsRun (self,html):
        for plugin in self.__plugins:
            plugin(html)

    def getHtml (self,url):
        try:
            if url not in self.__wholeList:
                self.__wholeList.append(url)
            else:
                return ""

            if self.__currentDepth > self.__maxDepth:
                return ""

            print("climbing %s" % (url))

            if self.__prot == "":
                if url.startswith("https:"):
                    self.__prot = "https:"
                else:
                    self.__prot = "http:"

            if self.__domain == "":
                d = re.findall("(http(?:s|):\/\/.+?)(?:[\/]|$)", url, re.DOTALL)
                if len(d) > 0:
                    self.__domain = d[0]

            request = Request(self.__encodeUri(url))

            for x in self.__config:
                if len(x) > 1:
                    request.add_header(x[0],x[1])

            response = urlopen(request)
            httpMessage = response.info()
            contentType = httpMessage.get_content_type()

            if contentType != "text/html" and contentType != "text/plain":
                print("%s | %s" % (url,"Not Html"))
                return ""

            serverCharset = httpMessage.get_content_charset()
            if serverCharset == None or serverCharset == "":
                serverCharset = "utf-8"

            html = self.__ungzip(response.read()).decode(serverCharset)
            return html

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error with %s at line %s: %s" % (url, exc_tb.tb_lineno, e))

    def getLink (self,urls):
        try:
            if len(urls) == 0:
                return

            urlList = urls[:self.__singlePageMaxTrace]
            
            self.__currentDepth += 1

            for url in urlList:
                if url.startswith("http"):
                    self.Run(url)
                elif url.startswith("//"):
                    self.Run(self.__prot + url)
                elif url.startswith("/"):
                    self.Run(self.__domain + url)
                elif url.startswith("#"):
                    print("%s | %s" % (self.__domain + url,"[Dynamic link]"))
                elif url.startswith("javascript"):
                    print("ignore %s" % (url))
                else:
                    self.Run(self.__domain + "/" + url)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error with %s at line %s: %s" % (url, exc_tb.tb_lineno, e))

    def __encodeUri (self,url):

        result = parse.urlparse(url)
        
        # 将 query 部分按照 / 切割,然后将每个元素进行编码
        # pathTmp = list(map(lambda tmp:quote(tmp),result.path.split("/")))
        pathTmp = [quote(tmp) for tmp in result.path.split("/")]

        queryTmp = []
        for item in result.query.split("&"):
            tmp = item.split("=")
            if len(tmp) > 1:
                queryTmp.append(quote(tmp[0]) + "=" + quote(tmp[1]))

        return parse.urlunparse(
            (result.scheme,result.netloc,'/'.join(pathTmp),result.params,'&'.join(queryTmp),result.fragment)
        )

    def __ungzip (self,data):
        data = gzip.decompress(data)
        return data

    def Run (self,url):
        html = self.getHtml(url)
        urls = self.filtersRun(html)
        if len(self.__plugins) > 0:
            self.__plugins(html)
        return self.getLink(urls)

if __name__ == '__main__':
    s = Spider()
    s.setConfig([("Accept-Encoding","gzip"),("Connection","keep-alive"),("Cache-Control","max-age=0")])
    s.setFilters(lambda html:re.findall('<a.+?href="(.+?)"', html, re.DOTALL))
    s.Run("http://www.acfun.tv/")
    