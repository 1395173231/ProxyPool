import base64
import re

from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
BASE_URL = 'http://free-proxy.cz/en/proxylist/country/HK/all/ping/all/{page}'
MAX_PAGE = 2


class FreeProxyCZCrawler(BaseCrawler):
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
        trs = doc('#proxy_list > tbody > tr').items()
        for tr in trs:
            # if tr.find('td:nth-child(1)').text() == "":
            #     continue
            host = tr.find('td:nth-child(1)').text()
            match = re.search(r'Base64\.decode\("([^"]*)"\)', host)

            # 如果找到匹配，提取出Base64编码
            if match:
                base64_str = match.group(1)
                host = base64.b64decode(base64_str).decode("utf-8")
            else:
                continue
            port = tr.find('td:nth-child(2)').text()
            if host == "" or port == "":
                continue
            yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = FreeProxyCZCrawler()
    for proxy in crawler.crawl():
        print(proxy)
