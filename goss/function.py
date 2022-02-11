#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""

from wush.config.function import FunctionFactory

from .config import GitTypeEnum
from .config import get_access_token

@FunctionFactory.register()
def get_github_access_token():
    """获取 github access_token"""
    return get_access_token(GitTypeEnum.GITHUB.value)
