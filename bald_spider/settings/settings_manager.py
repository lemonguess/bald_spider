#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024-04-23 18:48
@Author  : lxc
@File    : setting_manager.py
@Desc    :

"""
from copy import deepcopy
from importlib import import_module
from collections.abc import MutableMapping
from bald_spider.settings import default_settings


class SettingsManager(MutableMapping):
    def __init__(self, values=None):
        self.attributes = {}
        self.set_settings(default_settings)
        self.update_values(values)

    def __getitem__(self, item):
        if item not in self:
            return None
        return self.attributes[item]

    def get(self, key, default=None):
        return self[key] if key in self else default

    def getint(self, name, default=0):
        return int(self.get(name, default))

    def getfloat(self, name, default=0.0):
        return float(self.get(name, default))

    def getbool(self, name, default=False):  # noqa
        got = self.get(name, default)
        try:
            return bool(int(got))  # 处理"False", "True",抛出ValueError
        except ValueError:
            if got in ("True", "true", "TRUE"):
                return True
            elif got in ("False", "false", "FALSE"):
                return False
            raise ValueError(
                "Supported values for bool settings are (0 or 1),(True, False),"
                "('0','1'), ('True' or 'False'), ('true' or 'false') or ('TRUE' or 'FALSE')"
            )

    def getlist(self, name, default=None):
        value = self.get(name, default or [])
        if isinstance(value, str):
            value = value.split(',')
        return list(value)

    def __contains__(self, item):
        return item in self.attributes

    def __setitem__(self, key, value):
        self.set(key, value)

    def set(self, key, value):
        self.attributes[key] = value

    def __delitem__(self, key):
        del self.attributes[key]

    def delete(self, key):
        del self.attributes[key]

    def set_settings(self, module):
        """把settings.py中的变量加载到self.attributes"""
        if isinstance(module, str):
            module = import_module(module)
        for key in dir(module):
            if key.isupper():
                self.set(key, getattr(module, key))

    def __str__(self):
        return f"<Settings values-{self.attributes}>"

    __repr__ = __str__

    def __iter__(self):
        return iter(self.attributes)

    def __len__(self):
        return len(self.attributes)

    def update_values(self, values):
        if values is not None:
            for key, value in values.items():
                self.set(key, value)

    def copy(self):
        return deepcopy(self)


if __name__ == '__main__':
    settings = SettingsManager()
    settings["CONCURRENCY"] = 8
    print(settings.items())
