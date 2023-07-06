from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler

BASE_URL = 'https://scrapingant.com/proxies'
MAX_PAGE = 1


class ScrapingAntCrawler(BaseCrawler):
    """
    daili66 crawler, http://www.66ip.cn/1.html
    """
    urls = [BASE_URL]

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        trs = doc('.proxies-table > tr').items()
        for tr in trs:
            host = tr.find('td:nth-child(1)').text()
            port = tr.find('td:nth-child(2)').text()
            if host == "" or port == "":
                continue
            yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = ScrapingAntCrawler()
    for proxy in crawler.crawl():
        print(proxy)
