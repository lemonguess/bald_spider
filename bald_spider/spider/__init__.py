from bald_spider import Request


class Spider:
    def __init__(self):
        if not hasattr(self, 'start_urls'):
            self.start_urls = []
        self.crawler = None

    @classmethod
    def create_instance(cls, crawler):
        o = cls()
        o.crawler = crawler
        return o

    def start_requests(self):
        if self.start_urls:
            if isinstance(getattr(self, 'start_urls'), str):
                yield getattr(self, 'start_urls')
            for url in self.start_urls:
                yield Request(url=url)
        else:
            # 兼容只有start_url属性，仅代表一个地址的字符串
            if hasattr(self, 'start_url') and isinstance(getattr(self, 'start_url'), str):
                yield getattr(self, 'start_url')

    def parse(self, response):
        raise NotImplemented

    def __str__(self):
        return self.__class__.__name__
