#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024-04-25 0:56
@Author  : lxc
@File    : __init__.py.py
@Desc    :

"""
from abc import ABCMeta


class Field(dict):
    pass


class ItemMeta(ABCMeta):
    def __new__(mcs, name, bases, attrs):
        field = {}
        for key, value in attrs.items():
            if isinstance(value, Field):
                field[key] = value
        cls_instance = super().__new__(mcs, name, bases, attrs)
        cls_instance.Field = field
        return cls_instance
