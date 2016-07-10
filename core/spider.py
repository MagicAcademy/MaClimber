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

    def ungzip(self, data):
        """
        解压回传的html b数据
        :param data:
        :return:
        """
        try:
            print('unzip HTML...')
            data = gzip.decompress(data)
            print('finished')
        except:
            print('No need to be unzipped,pass...')
        return data

    def get_html(self, url, rtn_type='soup'):
        """
        一次获取html页面,以备后用
        :param rtn_type: 返回数据类型
        :return: 纯html / BeautifulSoup封装的类
        """
        if url == '':
            url = self.url
        # 声明cookie容器
        cj = http.cookiejar.CookieJar()
        # 声明cookie处理器
        proc = urllib.request.HTTPCookieProcessor(cj)
        # 利用处理过后的cookie构建cookie类型的url开瓶器
        opener = urllib.request.build_opener(proc)
        result = []
        if self.header != "":
            for key, value in self.header.items():
                elem = (key, value)
                result.append(elem)
        opener.addheaders = result
        # 开瓶拿数据
        op = opener.open(url)
        # 看页面编码
        http_message = op.info()
        coding = http_message.get_content_charset()
        if coding is None or coding == "":
            coding = "utf-8"
        data = op.read()
        # 解压解码
        data = self.ungzip(data).decode(coding)
        if rtn_type == 'soup':
            return BeautifulSoup(data, "html.parser")
        else:
            return data

    def get_links(self, maxcurrent_depth, whole_list=[]):
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

    def find_by_regx(self, source, regx):
        """
        根据正则获取内容
        :param source: 内容源
        :param regx: 筛选正则
        :return: 返回结果str
        """
        if isinstance(source, BeautifulSoup):
            # todo soup对象的元素内容提取
            pass
        else:
            return re.search(regx, source).group()

    def find_all_by_regx(self, source, regx):
        """
        根据正则获取所有内容
        :return:返回结果array
        """
        if isinstance(source, BeautifulSoup):
            pass
        else:
            return re.compile(regx).findall(source)

