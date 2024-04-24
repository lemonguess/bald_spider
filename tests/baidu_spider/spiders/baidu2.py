from bald_spider import Request
from bald_spider.spider import Spider


class BaiduSpider(Spider):
    start_urls = ['https://www.baidu.com']

    # start_url = 'https://www.baidu.com'
    async def parse(self, response):
        print("parse2", response)
        for i in range(200):
            url = "https://www.baidu.com"
            request = Request(url=url, callback=self.parse_page)
            yield request
    def parse_page(self, response):
        print("parse_page2", response)
        for i in range(10):
            url = "https://www.baidu.com"
            requetst = Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        print('parse_detail2', response)
