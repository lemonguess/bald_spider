from bald_spider import Request
from bald_spider.spider import Spider
from items import BaiduItem  # noinspection


class BaiduSpider(Spider):
    start_urls = ['https://www.baidu.com']
    custom_settings = {'CONCURRENCY': 8}

    # @classmethod
    # def crawl(cls):
    #     # 实例化的逻辑
    #     return cls()
    # start_url = 'https://www.baidu.com'
    def parse(self, response):
        print("parse", response)
        for i in range(10):
            url = "https://www.baidu.com"
            request = Request(url=url, callback=self.parse_page)
            yield request

    def parse_page(self, response):
        print("parse_page", response)
        for i in range(10):
            url = "https://www.baidu.com"
            request = Request(url=url, callback=self.parse_detail)
            yield request

    def parse_detail(self, response):
        # print('parse_detail', response)
        item = BaiduItem()
        item['url'] = 'baidu.com'
        item['title'] = '百度首页'
        yield item
