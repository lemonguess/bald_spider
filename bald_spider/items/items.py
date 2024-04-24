#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024-04-25 0:56
@Author  : lxc
@File    : items.py
@Desc    :

"""
from copy import deepcopy
from pprint import pformat
from collections.abc import MutableMapping
from bald_spider.items import Field, ItemMeta



class Item(MutableMapping, metaclass=ItemMeta):
    FIELDS: dict

    def __init__(self):
        self._values = {}

    def __setitem__(self, key, value):
        if key in self.FIELDS:
            self._values[key] = value
        else:
            raise KeyError(f"{self.__class__.__name__} does not support field: `{key}`")

    def __getattr__(self, item):
        # 在获取不到属性的时候会触发
        raise AttributeError(
            f"{self.__class__.__name__} does not support attribute: `{item}`. "
            f"Please add the `{item}` field to the `{self.__class__.__name__}, "
            f"and use item[{item!r}] to get field value"
        )

    def __getattribute__(self, item):
        """属性拦截器"""
        field = super().__getattribute__("FIELDS")
        if item in field:
            raise AttributeError(f"use item[{item!r}] to get field value.")
        else:
            return super().__getattribute__(item)

    def __getitem__(self, item):
        return self._values[item]

    def __delitem__(self, key):
        del self._values[key]

    def __setattr__(self, key, value):
        if not key.startswith("_"):
            raise AttributeError(f"use item[{key!r}] = {value!r} to set field value.")
        super().__setattr__(key, value)

    def __repr__(self):
        return pformat(dict(self))

    __str__ = __repr__

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)
    def to_dict(self):
        return dict(self)
    def copy(self):
        return deepcopy(self)
if __name__ == '__main__':
    class TestItem(Item):
        url = Field()
        title = Field()


    test_item = TestItem()
    test_item['url'] = 'http://www.baidu.com'
    print(test_item['url'])
    print(test_item.xxx)
