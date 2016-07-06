#!/usr/bin/env python
import http.cookiejar
import gzip
import urllib.request
from bs4 import BeautifulSoup


class Spider(object):
    """
    爬虫类,含有抽象的公用方法
    """

    def __init__(self, url, header):
        self.url = url
        self.header = header

    def getHtml(self, type='soup', coding='utf-8'):
        cj = http.cookiejar.CookieJar()
        proc = urllib.request.HTTPCookieProcessor(cj)
        opener = urllib.request.build_opener(proc)
        result = []
        for key, value in self.header.items():
            elem = (key, value)
            result.append(elem)
        opener.addheaders = result
        op = opener.open(self.url)
        data = op.read()
        data = self.ungzip(data).decode(coding)
        if type=='soup':
            return BeautifulSoup(data, "html.parser")
        else:
            return data.replace('\n', '')

    def ungzip(self, data):
        try:
            print('unzip HTML...')
            data = gzip.decompress(data)
            print('finished')
        except:
            print('No need to be unzipped,pass...')
        return data



