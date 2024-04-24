#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024-04-22 2:47
@Author  : lxc
@File    : exceptions.py
@Desc    :
定义异常类型
"""


class TransformTypeError(TypeError):
    pass


class OutputError(Exception):
    pass


class SpiderTypeError(TypeError):
    pass
