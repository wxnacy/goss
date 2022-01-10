#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
配置模块
"""
#  import os

from wpy.base import BaseEnum
from wpy.path import (
    read_dict, write_dict
)

from .constants import Constants


class GitTypeEnum(BaseEnum):
    GITHUB = 'github'

def get_access_token(git_type, version=None):
    """获取 access_token"""
    data = {}
    try:
        data = read_dict(Constants.CREDENTIALS_PATH) or {}
    except:
        pass
    token = data.get(git_type) or {}
    access_token = token.get('access_token')
    if version:
        if token.get("version") == version:
            return access_token
        else:
            return None
    else:
        return access_token

def save_github_access_token(version, access_token):
    """保存"""
    data = {}
    try:
        data = read_dict(Constants.CREDENTIALS_PATH) or {}
    except:
        pass
    data[GitTypeEnum.GITHUB.value] = {
        "version": version, "access_token": access_token, }
    write_dict(Constants.CREDENTIALS_PATH, data)
