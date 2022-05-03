#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

import base64

from wush.cli.run import run as run_wush
from wush.cli.run import run_in_shell
from .constants import Constants

class Module():
    API_GITHUB = 'api_github'
    WWW_GITHUB = 'www_github'

class Request():
    OAUTH_ACCESS_TOKEN = 'oauth_access_token'
    OAUTH_AUTHORIZE = 'oauth_authorize'

    CREATE_CONTENT = 'create_content'
    GET_CONTENT = 'get_content'
    DELETE_CONTENT = 'delete_content'

class Command():
    OAUTH_ACCESS_TOKEN = f'--module {Module.API_GITHUB} --name {Request.OAUTH_ACCESS_TOKEN}'


_wush_params = { "config": Constants.CONFIG_PATH }
print(_wush_params)

class Github(object):

    def __init__(self, owner=None, repo=None):
        self.owner = owner
        self.repo = repo

    #  def oauth_access_token(self, code, client_id=None, client_secret=None):
        #  params={
            #  "code": code,
            #  }
        #  if client_id:
            #  params['client_id'] = client_id
        #  if client_secret:
            #  params['client_secret'] = client_secret
        #  return run_wush(Module.WWW_GITHUB, Request.OAUTH_ACCESS_TOKEN,
            #  params = params, **_wush_params)

    def oauth_authorize(self, client_id=None, scope=None, redirect_uri=None):
        params={ }
        if client_id:
            params['client_id'] = client_id
        if scope:
            params['scope'] = scope
        if redirect_uri:
            params['redirect_uri'] = redirect_uri

        return run_in_shell(Module.WWW_GITHUB, Request.OAUTH_AUTHORIZE,
            params=params, **_wush_params)

    def create_file(self, path, content=None, message='', filepath=None,
            sha=None):
        """创建或修改文件
        :params str path: repo 文件地址
        :params str content: 文件内容，需要 Base64 编码
        :params str message: 提交信息
        :params str filepath: 本地文件路径
        :params str sha: 需要修改文件的 sha 签名
        """
        if content == None and not filepath:
            raise ValueError('content or filepath must set one')

        if content == None and filepath:
            byte_data = None
            with open(filepath, 'rb') as f:
                byte_data = f.read()
            content = base64.b64encode(byte_data).decode()

        json_data = { "message": message, "content": content }
        if sha:
            json_data['sha'] = sha
        res = run_wush(Module.API_GITHUB, Request.CREATE_CONTENT,
            json = json_data,
            env = {
                "path": path ,
                "owner": self.owner,
                "repo": self.repo},
            **_wush_params
        )
        return res

    def get_file(self, path):
        """获取文件
        :params str path: repo 文件地址
        """
        res = run_wush(Module.API_GITHUB, Request.GET_CONTENT,
            env = {
                "path": path ,
                "owner": self.owner,
                "repo": self.repo},
            **_wush_params
        )
        return res

    def delete_file(self, path, sha, message=''):
        """获取文件
        :params str path: repo 文件地址
        """
        #  get_file_res = self.get_file(path)
        #  print(get_file_res.status_code, get_file_res.json())
        #  sha = get_file_res.json().get("sha")
        json_data = { "message": message, "sha": sha }
        res = run_wush(Module.API_GITHUB, Request.DELETE_CONTENT,
            env = {
                "path": path ,
                "owner": self.owner,
                "repo": self.repo},
            json = json_data,
            **_wush_params
        )
        return res

    def get_download_url(self, path):
        return f'https://raw.githubusercontent.com/{self.owner}'\
                f'/{self.repo}/master/{path}'

