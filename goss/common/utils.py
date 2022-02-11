#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""


def get_current_module_path():
    """获取当前模块的路径"""
    import goss as _module
    module_path = _module.__path__[0]
    return module_path
