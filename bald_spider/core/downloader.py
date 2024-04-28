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
import random
from contextlib import asynccontextmanager  # 上下文协议工具
from typing import Final, Set, Optional
from aiohttp import ClientSession, TCPConnector, BaseConnector, ClientTimeout, ClientResponse, TraceConfig

from bald_spider.utils.log import get_logger
from bald_spider import Response


class ActiveRequestManager:
    def __init__(self):
        self._active: Final[Set] = set()

    def add(self, request):
        print("add", request)
        self._active.add(request)

    def remove(self, request):
        print("remove", request)
        self._active.remove(request)

    def __len__(self):
        return len(self._active)

    @asynccontextmanager
    async def __call__(self, request):
        """类实例可以像函数一样调用"""
        try:
            yield self.add(request)
        finally:
            self.remove(request)


class Downloader:
    def __init__(self, crawler):
        self.crawler = crawler
        self._active = ActiveRequestManager()
        self.session: Optional[ClientSession] = None
        self.connector: Optional[BaseConnector] = None
        self._verify_ssl: Optional[bool] = None
        self._timeout: Optional[ClientTimeout] = None
        self.use_session: Optional[bool] = None

        self.logger = get_logger(self.__class__.__name__, self.crawler.settings.get("LOG_LEVEL"))
        self.request_method = {
            'get': self._get,
            'post': self._post
        }

    def open(self):
        self.logger.info(
            f"{self.crawler.spider} <downloader class: {type(self).__name__}>"
            f"<concurrency>: {self.crawler.settings.get('CONCURRENCY')}"
        )
        request_timeout = self.crawler.settings.getint("REQUEST_TIMEOUT")
        self._timeout = ClientTimeout(total=request_timeout)
        self._verify_ssl = self.crawler.settings.getbool("VERIFY_SSL")
        self.use_session = self.crawler.settings.getbool("USE_SESSION")
        if self.use_session:
            self.connector = TCPConnector(verify_ssl=self._verify_ssl)
            trace_config = TraceConfig()
            trace_config.on_request_start.append(self.request_start)
            self.session = ClientSession(connector=self.connector, timeout=self._timeout, trace_configs=[trace_config])

    async def fetch(self, request) -> Optional[Response]:
        async with self._active(request):
            response = await self.download(request)
            return response

    async def download(self, request) -> Response:
        try:
            if self.use_session:
                response = await self.send_request(self.session, request)
                body = await response.content.read()
            else:
                connector = TCPConnector(verify_ssl=self._verify_ssl)
                trace_config = TraceConfig()
                trace_config.on_request_start.append(self.request_start)
                async with ClientSession(connector=connector, timeout=self._timeout,
                                         trace_configs=[trace_config]) as session:
                    response = await self.send_request(session, request)
                    body = await response.content.read()

        except Exception as exc:
            self.logger.error(f"Error during request: {exc}")
            raise exc
        return self.structure_response(request, response, body)

    @staticmethod
    def structure_response(request, response, body):
        return Response(
            url=response.url,
            headers=dict(response.headers),
            status=response.status,
            body=body,
            request=request
        )

    async def send_request(self, session, request) -> ClientResponse:

        return await self.request_method[request.method.lower()](session, request)

    @staticmethod
    async def _get(session, request) -> ClientResponse:
        response = await session.get(
            request.url, headers=request.headers, cookies=request.cookies, proxy=request.proxy
        )
        return response

    @staticmethod
    async def _post(session, request) -> ClientResponse:
        response = await session.post(
            request.url, data=request.body, headers=request.headers, cookies=request.cookies, proxy=request.proxy
        )
        return response

    async def request_start(self, _session, _trace_config_ctx, params):
        self.logger.debug(f"request downloading: {params.url}, method: {params.method}")

    def idle(self) -> bool:
        return len(self._active) == 0

    def __len__(self):
        return len(self._active)

    async def close(self):
        if self.connector:
            await self.connector.close()
        if self.session:
            await self.session.close()
