#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import urllib2
import re


def log(content):
    print "[log] %s" % content


def getlink(url, cookie=""):
    try:
        requestBody = urllib2.Request(url)
        requestBody.add_header("Cookie", cookie)
        requestBody.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36")
        requestBody.add_header("Referer", "http://www.javlibrary.com/")
        response = urllib2.urlopen(requestBody)

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
