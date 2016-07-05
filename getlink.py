#!/usr/bin/env python

from urllib.request import urlopen
import re
import sys, os
from urllib.parse import quote

maxDepth = 5  # Max trace depth
singlePageMaxTrace = 10  # Single page link trace limit

wholeList = []

def log(content):
    print("%s" % content)


def startclimb(url, cookie=""):
    log("MaClimber demo start.")
    log("====Start climbing====")
    log("Start with: %s" % url)
    log("Max depth: %s" % maxDepth)
    log("======================")
    getlink(url,cookie)


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

        # response = urlopen(quote(url))
        response = urlopen(url)
        http_message = response.info()
        contentType = http_message.get_content_type()
        if (contentType != "text/html") and (contentType != "text/plain"):
            log("%s %s | %s" % (depthPrefix, url, "Not HTML"))
            return


        serverCharset = http_message.get_content_charset()
        if serverCharset == None or serverCharset == "":
            serverCharset = "utf-8"
        html = response.read().decode(serverCharset)
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
    startclimb("http://stackoverflow.com/")

