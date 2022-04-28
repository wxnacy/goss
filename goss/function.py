#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""

from wush.config.function import FunctionFactory
from wush.config.function import load_super_function
from wush.web.response import ResponseHandler

from .config import GitTypeEnum
from .config import get_access_token

super_function = load_super_function()

@FunctionFactory.register()
def get_github_access_token():
    """获取 github access_token"""
    return get_access_token(GitTypeEnum.GITHUB.value)


@ResponseHandler.register('api_github', 'get_content')
def handler_res_get_content(response):
    """TODO: Docstring for handler_res_get_content.

    :arg1: TODO
    :returns: TODO

    """
    output = {
        "headers": [
            #  { "display": "列名", 'width': '列宽度，非必传' }
            { "display": "文件名", 'width': 30},
            { "display": "路径"},
            { "display": "类型"},
        ],
        "items": [ ]
    }

    data = response.json()
    if isinstance(data, dict):
        data = [data]
    for line in data:
        op_line = (
            line.get("name"), line.get('path'), line.get("type"))
        output['items'].append(op_line)
    super_function.print_table(output)

@FunctionFactory.register()
def handler_response(response):
    argument = response.request_builder.argument

    super_function.handler_response(response)
