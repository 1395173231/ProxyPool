from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler

BASE_URL = 'https://www.freeproxy.world/?type=&anonymity=&country=HK&speed=&port=&page={page}'
MAX_PAGE = 2


class FreeProxyCrawler(BaseCrawler):
    """
    daili66 crawler, http://www.66ip.cn/1.html
    """
    urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE + 1)]

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        trs = doc('.layui-table > tbody > tr').items()
        for tr in trs:
            # if tr.find('td:nth-child(1)').text() == "":
            #     continue
            host = tr.find('td:nth-child(1)').text()
            port = tr.find('td:nth-child(2)').text()
            if host == "" or port == "":
                continue
            yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = FreeProxyCrawler()
    for proxy in crawler.crawl():
        print(proxy)
