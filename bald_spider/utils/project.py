#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024-04-23 18:46
@Author  : lxc
@File    : project.py
@Desc    :

"""
import os.path
import sys

from bald_spider.settings.settings_manager import SettingsManager


def _get_closest(path='.'):
    path = os.path.abspath(path)
    return path


def _init_env():
    closest = _get_closest()
    if closest:
        project_dir = os.path.dirname(closest)
        sys.path.append(project_dir)


def get_settings(settings='settings'):
    # _settings = SettingsManager()
    _settings = SettingsManager({'1':2})
    _init_env()
    _settings.set_settings(settings)
    return _settings
def merge_settings(spider, settings):
    if hasattr(spider, "custom_settings"):
        custom_settings = getattr(spider, "custom_settings")
        settings.update_values(custom_settings)