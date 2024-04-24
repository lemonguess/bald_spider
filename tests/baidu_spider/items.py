#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024-04-25 0:57
@Author  : lxc
@File    : items.py
@Desc    :

"""
from bald_spider.items import Field
from bald_spider import Item


class BaiduItem(Item):
    url = Field()
    title = Field()
