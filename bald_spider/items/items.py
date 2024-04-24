#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024-04-25 0:56
@Author  : lxc
@File    : items.py
@Desc    :

"""
from bald_spider.items import Field, ItemMeta

class Item(metaclass=ItemMeta):
    FIELDS: dict

    def __init__(self):
        # for cls_attr, value in self.__class__.__dict__.items():
        #     if isinstance(value,Field):
        #         self.FIELDS[cls_attr] = value
        self._values = {}


    def __setitem__(self, key, value):
        if key in self.FIELDS:
            self._values[key] = value
        else:
            raise KeyError(f"{self.__class__.__name__} does not support field: `{key}`")
    def __repr__(self):
        return str(self._values)

if __name__ == '__main__':
    class TestItem(Item):
        url = Field()
        title = Field()
    test_item = TestItem()
    test_item['url'] = 'http://www.baidu.com'
    test_item['name'] = 'dasfdsa'