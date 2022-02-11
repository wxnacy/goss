#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
常量模块
"""

import os

from goss.common.utils import get_current_module_path

class Constants(object):
    CONFIG_PATH = os.path.join(get_current_module_path(),
        'resources/config/config.yml')
    CREDENTIALS_PATH = os.path.expanduser('~/.goss-credentials')
