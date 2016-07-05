#!/usr/bin/env python

from urllib.request import urlopen
import re


def log(content):
    print("[log] %s" % content)


def getlink(url, cookie=""):
    log("Get hyperlinks from: %s" % url)
    try:
        response = urlopen(url)

        m = re.findall('<a.+?href="(.+?)"', response.read().decode("utf-8"), re.DOTALL)

        if len(m) < 1:
            log("No link found")
        else:
            list = []
            for x in m:
                if x not in list:
                    list.append(x)
            for item in list:
                log(item)

    except Exception as e:
        log("Error with %s: %s" % (url, e))

if __name__ == "__main__":
    getlink("a~.com")
    getlink("https://www.bilibili.com")
