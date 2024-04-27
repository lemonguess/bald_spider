#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024-04-26 14:12
@Author  : lxc
@File    : download.py
@Desc    :
aiohttp httpx 插件化设计：插拔型，即插即用。
"""
import asyncio
import time
import random


class Downloader:
    def __init__(self):
        self._active = set()

    async def fetch(self, request):
        self._active.add(request)
        response = await self.download(request)
        self._active.remove(request)
        return response

    async def download(self, request):
        await asyncio.sleep(random.uniform(0, 1))
        return "result"

        # response = requests.get(request.url)
        # print(response)

    def idle(self) -> bool:
        return len(self._active) == 0

    def __len__(self):
        return len(self._active)
