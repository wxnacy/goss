#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""

from wush.config.function import FunctionFactory
from wush.config.function import load_super_function
from wush.web.response import ResponseHandler

from goss.github.constants import (
    MODULE_WWW,
    REQUEST_OAUTH_ACCESS_TOKEN
)
from .config import (
    GitTypeEnum,
    get_access_token,
    save_github_access_token
)
from .models import Github
from .wushtools import run_in_shell

super_function = load_super_function()

@FunctionFactory.register()
def get_github_access_token():
    """获取 github access_token"""
    return get_access_token(GitTypeEnum.GITHUB.value)

@FunctionFactory.register()
def github_callback(code, version):
    """获取 github access_token"""
    run_in_shell(MODULE_WWW, REQUEST_OAUTH_ACCESS_TOKEN, params = { "code": code })
    return '登陆成功'


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
