#!/usr/bin/env python

from urllib.request import urlopen
import re


def log(content):
    print("[log] %s" % content)


def getlink(url, cookie=""):
    try:
        response = urlopen(url)

        m = re.findall('<a.+?href="(.+?)"', response.read().decode("utf-8"), re.DOTALL)
        if len(m) < 1:
            log("No link found")
        else:
            for x in m:
                log(x)
    except Exception:
        log("Error")

if __name__ == "__main__":
    getlink("https://www.bilibili.com")
