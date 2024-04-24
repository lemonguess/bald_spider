#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024-04-23 0:39
@Author  : lxc
@File    : demo1.py
@Desc    :

"""
import asyncio
from asyncio import Semaphore, BoundedSemaphore
semaphore = Semaphore(5)
async def demo():
    await semaphore.acquire()
    print('11111111111')
    semaphore.release()
    await semaphore.acquire()
    print('22222222222')
    await semaphore.acquire()
    print('33333333333')
    await semaphore.acquire()
    print('44444444444')
    await semaphore.acquire()
    print('55555555555')
    await semaphore.acquire()
    print('66666666666')
asyncio.run(demo())