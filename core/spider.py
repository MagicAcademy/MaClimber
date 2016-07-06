#!/usr/bin/env python
import http.cookiejar
import gzip
import urllib.request
import sys,re
from bs4 import BeautifulSoup


class Spider(object):

    """
    爬虫母皇,含有抽象的公用方法
    """
    def __init__(self, url, header, max_depth=0):
        self.url = url
        self.header = header
        self.maxDepth = max_depth

    def getHtml(self, rtn_type='soup', coding='utf-8'):
        cj = http.cookiejar.CookieJar()
        proc = urllib.request.HTTPCookieProcessor(cj)
        opener = urllib.request.build_opener(proc)
        result = []
        if self.header != "":
            for key, value in self.header.items():
                elem = (key, value)
                result.append(elem)
        opener.addheaders = result
        op = opener.open(self.url)
        http_message = op.info()
        coding = http_message.get_content_charset()
        if coding == None or coding == "":
            coding = "utf-8"
        data = op.read()
        data = self.ungzip(data).decode(coding)
        if rtn_type == 'soup':
            return BeautifulSoup(data, "html.parser")
        else:
            return data


    def ungzip(self, data):
        try:
            print('unzip HTML...')
            data = gzip.decompress(data)
            print('finished')
        except:
            print('No need to be unzipped,pass...')
        return data


    def getLink(self, maxcurrent_depth, whole_list=[]):
        '''
        @SDD 纯爬虫方法 需要抽象
        :param maxcurrent_depth:
        :param whole_list:
        :return:
        '''
        try:
            pass
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error with %s at line %s: %s" % (self.url, exc_tb.tb_lineno, e))


    def getTitle(self, htmlcontent):
        m = re.findall('<title>(.+?)</title>', htmlcontent, re.DOTALL)
        if len(m) < 1:
            return "No title"
        else:
            return m[0]
