#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""
import os
import pyperclip
import json
from csarg import Action

from wpy import echo
from wpy.path import walkfile
from wush.config.function import print_table

from goss.models import Github
from goss import utils
from .command import CmdArgumentParser
from .command import CommandArgumentParserFactory


@CommandArgumentParserFactory.register()
class FileArgumentParser(CmdArgumentParser):
    cmd = 'file'

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('--create', action = Action.STORE_TRUE.value,
                help='repo owner')
        item.add_argument('--delete', action = Action.STORE_TRUE.value,
                help='删除文件')
        item.add_argument('--list', action = Action.STORE_TRUE.value,
                help='展示文件列表')
        item.add_argument('--owner', help='repo owner')
        item.add_argument('--repo', help='repo name')
        item.add_argument('--path', help='repo path')
        item.add_argument('--file', help='file path')

        item.git = Github()

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
        repo = args.repo
        owner = args.owner
        if '/' in repo:
            owner, repo = repo.split('/')
        self.git.owner = owner
        self.git.repo = repo
        if args.create:

            filepath = args.file
            path = args.path
            pathes = utils.format_repo_pathes(filepath, path)
            if os.path.isfile(filepath):
                self.upload_file(owner, repo, pathes[0], filepath)
            else:
                for i, _filepath in enumerate(walkfile(filepath)):
                    self.upload_file(owner, repo, pathes[i], _filepath)

        if args.delete:
            download_url = self.git.get_download_url(args.path)
            echo.info(f'Delete : {echo.blue(download_url)}')
            if not self.confirm(f'Are you sure delete {args.path}'):
                echo.echo(echo.yellow('Cancel delete!'))
                return
            get_file_res = self.git.get_file(args.path)
            if get_file_res.status_code == 404:
                echo.echo(echo.red('Fail: 文件不存在!'))
                return
            self.git.delete_file(args.path, get_file_res.json().get("sha"))
            echo.echo(echo.cyan('Success!'))

        if args.list:
            get_file_res = self.git.get_file(args.path)
            print(json.dumps(get_file_res.json(), indent=4))

            output = {
                "headers": [
                    #  { "display": "列名", 'width': '列宽度，非必传' }
                    { "display": "文件名", 'width': 30},
                    { "display": "路径"},
                    { "display": "类型"},
                ],
                "items": [ ]
            }

            data = get_file_res.json()
            if isinstance(data, dict):
                data = [data]
            for line in data:
                op_line = (
                    line.get("name"), line.get('path'), line.get("type"))
                output['items'].append(op_line)
            print_table(output)


    def upload_file(self, owner, repo, path, filepath):
        message = f"Create file {os.path.basename(filepath)}"
        echo.info(f'Upload : {filepath}')
        echo.info(f'Path   : {path}')
        download_url = f'https://raw.githubusercontent.com/{owner}'\
                f'/{repo}/master/{path}'
        echo.info(f'Url    : {echo.blue(download_url)}')
        try:
            # 将文件下载地址复制到粘贴板
            pyperclip.copy(download_url)
        except:
            # 忽略错误
            pass
        ctrl_v = echo.blue('<CTRL-V>')
        echo.info(f'Now you can use it with {ctrl_v} and wait for the upload to succeed.')

        try:
            echo.info('Waiting...')
            data = self.git.create_file(path, message = message,
                filepath = filepath)
            exists_msg = 'Invalid request.\n\n"sha" wasn\'t supplied.'
            if data.json().get("message") == exists_msg:
                if not self.confirm_replace():
                    echo.echo(echo.yellow('Cancel upload!'))
                    return
                echo.info('Waiting...')
                get_file_res = self.git.get_file(path)
                sha = get_file_res.json().get("sha")
                if not sha:
                    echo.echo(echo.red('Replace file failed!'))
                    return
                self.git.create_file(path, message = message,
                    filepath = filepath, sha = sha)
            echo.echo(echo.cyan('Success!'))
        except json.decoder.JSONDecodeError:
            echo.echo(echo.red('Upload failed!'))

    def confirm_replace(self):
        """确认上传替换"""
        confirm_msg = 'This file is exists. Do you want to replace?'
        echo.echo(echo.magenta(confirm_msg), end='')
        is_replace = input(' (y/n): ')
        if is_replace not in ('y', 'n'):
            return self.confirm_replace()
        return is_replace == 'y'

    def confirm(self, message):
        """确认上传替换"""
        echo.echo(echo.magenta(message), end='')
        is_yes = input(' (y/n): ')
        if is_yes not in ('y', 'n'):
            return self.confirm_replace()
        return is_yes == 'y'

    def run_shell(self, text):
        self.run_command(text)
