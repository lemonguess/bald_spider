import asyncio
from bald_spider import Request
from bald_spider.exceptions import OutputError
from bald_spider.items.items import Item
from bald_spider.spider import Spider
from bald_spider.core.downloader import Downloader
from bald_spider.core.schedule import Schedule
from typing import Optional, Generator, Callable
from inspect import iscoroutine
from bald_spider.utils.spider import transform
from bald_spider.task_manager import TaskManager


class Engine:
    def __init__(self, crawler):
        self.crawler = crawler
        self.settings = crawler.settings
        self.downloader: Optional[Downloader] = None
        self.scheduler: Optional[Schedule] = None
        self.spider: Optional[Spider] = None
        self.start_requests: Optional[Generator] = None
        self.task_manager: TaskManager = TaskManager(self.settings.getint('CONCURRENCY'))
        self.running = False

    async def start_spider(self, spider):
        self.running = True
        self.scheduler = Schedule()
        self.spider = spider
        if hasattr(self.scheduler, 'open'):
            self.scheduler.open()
        self.downloader = Downloader()
        self.start_requests = iter(spider.start_requests())  # iter函数可以接受一个可迭代对象作为参数，然后返回一个迭代器对象
        await self.open_spider()

    async def open_spider(self):
        crawling = asyncio.create_task(self.crawl())
        # 这里可以做其他事情
        await crawling

    async def crawl(self):
        """主逻辑"""
        while self.running:
            if (request := await self._get_next_request()) is not None:
                # 出队, 获取请求(若拿到request则请求)，否则else
                await self._crawl(request)
            else:
                try:
                    start_request = next(self.start_requests)  # noqa
                except StopIteration:
                    self.start_requests = None
                except Exception as exc:
                    # 1.发起请求的task须运行完毕；
                    # 2.调度器是否空闲；
                    # 3.下载器是否空闲.
                    if not await self._exit():
                        continue
                    else:
                        self.running = False
                else:
                    # 入队
                    await self.enqueue_request(start_request)

    async def _crawl(self, request):
        async def crawl_task():
            # 实现并发
            outputs = await self._fetch(request)
            # 处理outputs
            if outputs:
                await self._handle_spider_output(outputs)

        await self.task_manager.semaphore.acquire()
        self.task_manager.create_task(crawl_task())
        # asyncio.create_task(crawl_task())

    async def _fetch(self, request):
        async def _success(_response):
            callback: Callable = request.callback or self.spider.parse
            if _outputs := callback(_response):
                if iscoroutine(_outputs):
                    await _outputs
                else:
                    return transform(_outputs)

        _response = await self.downloader.fetch(request)
        outputs = await _success(_response)
        return outputs

    async def enqueue_request(self, request):
        await self._schedule_request(request)

    async def _schedule_request(self, request):
        # todo 去重
        await self.scheduler.enqueue_request(request)

    async def _get_next_request(self):
        return await self.scheduler.next_request()

    async def _handle_spider_output(self, outputs):
        async for spider_output in outputs:
            if isinstance(spider_output, Request):
                await self.enqueue_request(spider_output)
            elif isinstance(spider_output, Item):  # todo 需要判断是不是数据Item
                ...
            else:
                raise OutputError(f"{type(self.spider)} must return `Request` or `Item`")

    async def _exit(self):
        """
        1.发起请求的task须运行完毕；
        2.调度器是否空闲；
        3.下载器是否空闲.
        :return:
        """
        if self.scheduler.idle() and self.downloader.idle() and self.task_manager.all_done():
            return True
        return False
