#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
常量模块
"""

import goss
import os

from goss.common.utils import get_current_module_path

MODULE_PATH = goss.__path__[0]

WAPI_CONFIG_ROOT = os.path.join(MODULE_PATH, 'resources/config')

class Constants(object):
    CONFIG_PATH = os.path.join(get_current_module_path(),
        'resources/config/config.yml')


