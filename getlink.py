#!/usr/bin/env python

from urllib.request import urlopen
from urllib.request import Request
from urllib.request import quote
import urllib.parse as parse
import re
import sys, os
import gzip

maxDepth = 5  # Max trace depth
singlePageMaxTrace = 10  # Single page link trace limit

wholeList = []


def ungzip(data):
    try:
        data = gzip.decompress(data)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        log("Error at line %s: %s" % (exc_tb.tb_lineno, e))
    return data


def log(content):
    print("%s" % content)


def encode_uri(uri):
    result = parse.urlparse(uri)
    path_tmp = result.path.split('/')
    for index in range(len(path_tmp)):
        path_tmp[index] = quote(path_tmp[index])
    query_tmp = result.query.split('&')
    for index in range(len(query_tmp)):
        if query_tmp[index] == '':
            continue
        query_parm_tmp = query_tmp[index].split('=')
        query_tmp[index] = quote(query_parm_tmp[0]) + '=' + quote(query_parm_tmp[1])

    return parse.urlunparse(
        (result.scheme, result.netloc, '/'.join(path_tmp), result.params, '&'.join(query_tmp), result.fragment))


def startclimb(url, cookie=""):
    log("MaClimber demo start.")
    log("====Start climbing====")
    log("Start with: %s" % url)
    log("Max depth: %s" % maxDepth)
    log("======================")
    getlink(url, cookie)


def getlink(url, cookie, currentDepth=0):
    try:
        if url not in wholeList:
            wholeList.append(url)
        else:
            return

        if currentDepth > maxDepth:
            return

        depthPrefix = ""
        for _ in range(currentDepth):
            depthPrefix += "="
        depthPrefix += ">"

        prot = ""
        if url.startswith("https"):
            prot = "https:"
        else:
            prot = "http:"

        domain = ""
        d = re.findall("(http(?:s|):\/\/.+?)(?:[\/]|$)", url, re.DOTALL)
        domain = d[0]

        req = Request(encode_uri(url))
        req.add_header("Accept-Encoding", "gzip")
        req.add_header("Connection", "keep-alive")
        req.add_header("Cache-Control", "max-age=0")
        req.add_header("User-Agent",
                       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")

        response = urlopen(req)
        http_message = response.info()
        contentType = http_message.get_content_type()
        if (contentType != "text/html") and (contentType != "text/plain"):
            log("%s %s | %s" % (depthPrefix, url, "Not HTML"))
            return

        serverCharset = http_message.get_content_charset()
        if serverCharset == None or serverCharset == "":
            serverCharset = "utf-8"

        html = ungzip(response.read()).decode(serverCharset)
        m = re.findall('<a.+?href="(.+?)"', html, re.DOTALL)

        log("%s %s | %s" % (depthPrefix, url, gettitle(html)))

        if len(m) < 1:
            log("%s No link found to trace" % ("=" + depthPrefix))
        else:
            list = []
            for x in m:
                if x not in list:
                    list.append(x)
                if singlePageMaxTrace != 0 and len(list) >= singlePageMaxTrace:
                    break

            currentDepth += 1

            for item in list:
                if item.startswith("http"):
                    getlink(item, cookie, currentDepth)
                elif item.startswith("//"):  # need append a specific protocol
                    getlink(prot + item, cookie, currentDepth)
                elif item.startswith("#"):
                    log("%s %s | %s" % ("=" + depthPrefix, url + item, "[Dynamic link]"))
                elif item.startswith("/"):  # start with single "/", we should append domain to head
                    getlink(domain + item, cookie, currentDepth)
                elif item.startswith("javascript"):  # start with "javascript", we should ignore
                    log('ignore %s' % item)
                    continue
                else:
                    getlink(domain + "/" + item, cookie, currentDepth)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        log("Error with %s at line %s: %s" % (url, exc_tb.tb_lineno, e))


def gettitle(htmlcontent):
    m = re.findall('<title>(.+?)</title>', htmlcontent, re.DOTALL)
    if len(m) < 1:
        return "No title"
    else:
        return m[0]


if __name__ == "__main__":
    startclimb("http://www.runoob.com/")
