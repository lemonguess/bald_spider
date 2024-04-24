#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024-04-22 0:12
@Author  : lxc
@File    : pqueue.py
@Desc    :
优先级队列
"""
import asyncio
from asyncio import PriorityQueue, TimeoutError


class SpiderPriorityQueue(PriorityQueue):
    def __init__(self, maxsize=0):
        super(SpiderPriorityQueue, self).__init__(maxsize=maxsize)

    async def get(self):
        fut = super().get()
        try:
            return await asyncio.wait_for(fut, timeout=0.1)
        except TimeoutError:
            return None
