#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024-04-26 17:39
@Author  : lxc
@File    : response.py
@Desc    :

"""
import re
import ujson
from typing import Dict
from parsel import Selector
from urllib.parse import urljoin as _urljoin
from bald_spider import Request
from bald_spider.exceptions import DecodeError


class Response:
    def __init__(self,
                 url: str, *,
                 request: Request,
                 headers: Dict,
                 body: bytes = b"",
                 status: int = 200,
                 ):
        self.url = url
        self.request = request
        self.headers = headers
        self.body = body
        self.status = status
        self.encoding = request.encoding
        self._text_cache = None  # 若实际爬虫多次调用response.text,设置text_cache则无需多次处理
        self._selector = None

    @property
    def text(self) -> str:
        if self._text_cache:
            return self._text_cache
        try:
            self._text_cache = self.body.decode(self.encoding)
        except UnicodeDecodeError:
            try:
                _encoding_re = re.compile(r"charset=([\w-]+)", flags=re.I)
                _encoding_string = self.headers.get("Content-Type", "") or self.headers.get("content-type", "")
                _encoding = _encoding_re.search(_encoding_string)
                if _encoding:
                    _encoding = _encoding.group(1)
                    self._text_cache = self.body.decode(self.encoding)
                else:
                    raise DecodeError(f"{self.request}{self.request.encoding} error.")
            except UnicodeDecodeError as exc:
                raise UnicodeDecodeError(
                    exc.encoding, exc.object, exc.start, exc.end, f"{self.request}"
                )
        return self._text_cache

    def xpath(self, xpath_string):
        if self._selector is None:
            self._selector = Selector(text=self.text)
        return self._selector.xpath(xpath_string)

    def json(self):
        return ujson.loads(self.text)

    def urljoin(self, url: str) -> str:
        return _urljoin(self.url, url)

    def __str__(self):
        return f"<{self.status} {self.url}>"

    @property
    def meta(self):
        return self.request.meta
