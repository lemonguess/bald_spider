#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024-04-26 14:12
@Author  : lxc
@File    : log.py
@Desc    :

"""
from logging import Formatter, StreamHandler, INFO, Logger

LOG_FORMAT = f'%(asctime)s [%(name)s] %(levelname)s %(message)s'


class LoggerManage:
    logger = {}
    @classmethod
    def get_logger(cls, name: str = "default", log_level=None, log_format=LOG_FORMAT):
        key = (name, log_level)
        def gen_logger(log_format):
            log_format = Formatter(log_format)
            handler = StreamHandler()
            handler.setFormatter(log_format)
            handler.setLevel(log_level or INFO)
            _logger = Logger(name)
            _logger.addHandler(handler)
            _logger.setLevel(log_level or INFO)
            cls.logger[key] = _logger
            return _logger
        return cls.logger.get(key, None) or gen_logger(log_format)
get_logger = LoggerManage.get_logger

if __name__ == '__main__':
    log = LoggerManage()
    log.get_logger("")
