#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""
import os
import json
import multiprocessing as mp
from csarg import Action

from wpy import echo
from wush import run as run_wush

from goss.constants import Constants
from goss.models import Github
from goss.cli.server import run_server
from goss.config import get_access_token
from goss.function import get_github_access_token
from .command import CmdArgumentParser
from .command import CommandArgumentParserFactory


@CommandArgumentParserFactory.register()
class LoginArgumentParser(CmdArgumentParser):
    cmd = 'login'

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('--client-id', help='github client_id')
        item.add_argument('--client-secret', help='github client_secret')

        return item

    def get_completions_after_argument(self, word_for_completion):
        """
        获取补全的单词列表
        :param word_for_completion: 补全需要的单词
        """
        words = []
        if not self.argument:
            return words
        arg = self.argument
        if word_for_completion == '--name':
            # 针对 --name 参数的自动补全
            requests = self.config.get_requests(arg.module)
            words = []
            for req in requests:
                words.append(dict( text = req.name, display_meta=req.title))
            return words
        elif word_for_completion == '--env':
            # 环境变量
            # 使用当前请求的环境变量 keys 做补全
            request = self.config.get_request(arg.module, arg.name,
                    set_env=False)
            keys = environ_keys(request)
            self.logger.info(request.path)
            self.logger.info(
                f'request {arg.module} {arg.name} environ_keys {keys}')
            data = { f"{o}": "" for o in keys }

            words = self._dict_to_completions(data)
            return words

        return super().get_completions_after_argument(word_for_completion)

    def _dict_to_completions(self, data):
        """字典转为自动补全信息"""
        words = []
        for k, v in data.items():
            words.append(dict(
                text = '{}='.format(k),
                display = '{}={}'.format(k, v),
                display_meta=''))
        return words

    def run_command(self, text):
        """运行命令行模式"""
        args = self.parse_args(text)
        client_id = args.client_id
        client_secret = args.client_secret
        if not client_id:
            client_id = os.getenv('GOSS_CLIENT_ID')
        if not client_secret:
            client_secret = os.getenv('GOSS_CLIENT_SECRET')

        access_token = get_github_access_token()
        if access_token:
            echo.echo(echo.cyan('已登录!'))
            return

        p = mp.Process(target=run_server, daemon=True)
        p.start()
        try:
            version = client_id
            redirect_uri = f'http://localhost:3000/github/callback?version={version}'
            Github().oauth_authorize(client_id, redirect_uri = redirect_uri)
        except json.decoder.JSONDecodeError:
            pass

        while not access_token:
            access_token = get_github_access_token()

        p.terminate()
        echo.echo(echo.cyan('登录成功!'))


    def run_shell(self, text):
        pass
