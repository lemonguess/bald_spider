#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024-04-22 0:59
@Author  : lxc
@File    : request.py
@Desc    :

"""
from typing import Dict, Optional, Callable


class Request:
    def __init__(self,
                 url: str, *,  # *符号后面的参数是强制的关键字参数
                 headers: Optional[Dict] = None,
                 callback: Optional[Callable] = None,
                 priority: int = 0,  # 优先级队列的权重值
                 method: str = 'GET',
                 cookies: Optional[Dict] = None,
                 proxy: Optional[Dict] = None,
                 body='',
                 encoding: str = 'utf-8',
                 meta: Optional[Dict] = None
                 ):
        self.url = url
        self.headers = headers
        self.callback = callback
        self.priority = priority
        self.method = method
        self.cookies = cookies
        self.proxy = proxy
        self.body = body
        self.encoding = encoding
        self._meta = meta if meta is not None else {}

    def __str__(self):
        return f"{self.url} {self.method}"

    def __lt__(self, other):  # less than
        return self.priority < other.priority

    @property
    def meta(self):
        return self._meta
