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

    def setFilters (self,filter):
        self.__filters.append(filter)

    def setPlugin (self,plugin):
        self.__plugins.append(plugin)

    def setConfig (self,config):
        self.__config = config

    def getHtml (self,url):
        try:
            if url not in self.__wholeList:
                self.__wholeList.append(url)
            else:
                return ""

            if self.__currentDepth > self.__maxDepth:
                return ""

            print("climbing %s" % (url))

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

    def __encodeUri (self,url):

        result = parse.urlparse(url)
        
        # 将 query 部分按照 / 切割,然后将每个元素进行编码
        pathTmp = list(map(lambda tmp:quote(tmp),result.path.split("/")))

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
if __name__ == '__main__':
    s = Spider()
    # s.encodeUri("http://www.baidu.com/")
    s.setConfig([("Accept-Encoding","gzip"),("Connection","keep-alive"),("Cache-Control","max-age=0")])
    s.getHtml("http://www.baidu.com/")