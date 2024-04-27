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
from bald_spider import Request


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

    @property
    def text(self) -> str:
        try:
            text = self.body.decode(self.encoding)
        except UnicodeDecodeError:
            _encoding_re = re.compile(r"charset=([\w-]+)", flags=re.I)
            _encoding_string = self.headers.get("Content-Type", "") or self.headers.get("content-type", "")
            _encoding = _encoding_re.search(_encoding_string)
            if _encoding:
                _encoding = _encoding.group(1)
                text = self.body.decode(self.encoding)
            else:
                raise DecodeError("")
            return text


    def json(self):
        pass
        # return ujson.loads(self.body)
