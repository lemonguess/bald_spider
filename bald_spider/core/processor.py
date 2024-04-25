#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024-04-25 23:46
@Author  : lxc
@File    : processor.py
@Desc    :

"""
from typing import Union
from asyncio import Queue
from bald_spider import Request, Item


class Processor:
    def __init__(self, crawler):
        self.crawler = crawler
        self.queue: Queue = Queue()

    async def process(self):
        while not self.idle():
            result = await self.queue.get()
            if isinstance(result, Request):
                await self.crawler.engine.enqueue_request(result)
            else:
                assert isinstance(result, Item)
                await self._process_item(result)
    async def _process_item(self, item:Item):
        print(item)

    async def enqueue(self, output: Union[Request, Item]):
        await self.queue.put(output)
        await self.process()

    def idle(self) -> bool:
        return len(self) == 0

    def __len__(self):
        return self.queue.qsize()
