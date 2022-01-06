#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
工具模块
"""

import os

from wpy.path import walkfile

def format_repo_pathes(filepath, path=None):
    """格式化 repo 的地址列表
    :params str filepath: 本地文件路径
    :params str path: repo path

    1. filepath 为文件，path == None
        path = os.path.basename(filepath)
    2. filepath 为文件，path 为文件名
        path = path
    3. filepath 为文件，path 为文件夹名
        path = os.path.join(path, os.path.basename(filepath))
    4. filepath 为文件夹名，path == None
        以 filepath 文件夹为目录名，返回所有文件地址列表
    5. filepath 为文件夹名，path != None
        以 path 文件夹为目录名，返回所有文件地址列表
    """

    if os.path.isfile(filepath):
        if not path:
            return [os.path.basename(filepath)]
        if path.endswith('/'):
            return [os.path.join(path, os.path.basename(filepath))]
        return [path]

    dirname = os.path.basename(filepath) or  os.path.dirname(filepath)
    if path:
        dirname = os.path.join(path, dirname)
    origin_dir = os.getcwd()
    os.chdir(filepath)
    pathes = []
    for _path in walkfile('./'):
        _path = _path[2:]
        pathes.append(os.path.join(dirname, _path))
    os.chdir(origin_dir)
    return pathes
