import core.spider

if __name__ == "__main__":
    m = core.spider.Spider(url='http://www.stackoverflow.com/', header='')
    re = m.getHtml('raw')

