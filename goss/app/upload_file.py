#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

import click
from goss import Github
from goss import github_credential
from goss.app import utils
from goss.app.logger import Logger
import configparser
import os
import pyperclip
import sys

logger = Logger()


def upload_file(g, owner, repo, filepath, path, is_replace):
    '''上传文件'''
    logger.info('Upload file')
    logger.info('Source\t:', filepath)
    logger.info('Path\t:', path)
    download_url = f'https://raw.githubusercontent.com/{owner}/{repo}/master/{path}'
    html_url = f'https://github.com/{owner}/{repo}/blob/master/{path}'
    logger.info('HtmlUrl\t:', html_url)
    logger.info('DownUrl\t:', click.style(download_url, fg='blue'))
    try:
        # 将文件下载地址复制到粘贴板
        pyperclip.copy(download_url)
    except:
        # 忽略错误
        pass
    logger.info('Now you can use it with {} and wait for the upload to succeed.'.format(
        click.style('<CTRL-V>', fg='blue')
    ))
    logger.info('Waiting...')

    if filepath.startswith('http'):
        # 通过 url 上传
        default_create = g.create_file_from_url
    else:
        # 通过文件上传
        default_create = g.create_file_from_path

    # 上传文件
    code, data = default_create(owner, repo, filepath, path)
    if code == 404:
        utils.print_failed()
        logger.error('Repository Owner or Name not found', with_color=True)
        return

    # 如果文件已经存在，则询问是否覆盖
    if code == 422 and data.get("message") == \
            'Invalid request.\n\n"sha" wasn\'t supplied.':
        confirm_msg = 'This file is exists. Do you want to replace?'
        if not is_replace and not click.confirm(confirm_msg):
            return

        logger.warn('This file already exists and is now replaced',
                    with_color=True)

        logger.info('Waiting...')
        # 遇到重复文件名，需要获取 sha 值后进行覆盖
        code, data = g.get_file(owner, repo, path)
        sha = data['sha']
        code, data = default_create(owner, repo, filepath, path, sha)

        if code != 200:
            utils.print_failed()
            utils.print_error(data['message'])
            sys.exit(0)

@github_credential
def create(g, filepath, path=None, repo=None, yes=False, **kw):
    '''
    创建文件
    '''
    r = g.get_release()
    #  print(g._user)
    owner = g.owner
    if kw.get("config"):
        g.config.read(kw['config'])
    if not path:
        path = g.config.repo.path

    if not path:
        path = os.path.basename(filepath)

    if path.endswith('/'):
        path += os.path.basename(filepath)

    if not repo:
        repo = g.config.repo.name


    def _upload_asset():
        '''上传 release 的资产'''
        name = kw.get("name")
        if not name:
            name = os.path.basename(filepath)
        logger.info('Upload asset')
        logger.info('Release\t:', release)
        logger.info('Source\t:', filepath)
        #  logger.info('Path\t:', path)
        download_url = f'https://github.com/{owner}/{repo}/releases/download/{release}/{name}'
        html_url = f'https://github.com/{owner}/{repo}/blob/master/{path}'
        #  logger.info('HtmlUrl\t:', html_url)
        logger.info('DownUrl\t:', click.style(download_url, fg='blue'))
        pyperclip.copy(download_url)
        logger.info('Now you can use it with {} and wait for the upload to succeed.'.format(
            click.style('<CTRL-V>', fg='blue')
        ))
        logger.info('Waiting...')
        code, data = r.get_release_by_tag(owner, repo, release)
        if code == 404:
            utils.print_failed()
            logger.error('Release not found', with_color=True)
            sys.exit(0)

        release_id = data.get("id")

        code, data = r.upload_asset_from_path(owner, repo, release_id,
            filepath, name
        )
        if code != 201:
            utils.print_failed()
            utils.print_error(data['message'])
            for err in data.get('errors', []):
                utils.print_error(f"\t- {err['field']} {err['code']}")
            sys.exit(0)

    release = kw.get('release')
    if release:
        _upload_asset()
    else:
        upload_file(g, owner, repo, filepath, path, yes)
    utils.print_success()

@click.command()
@click.option('--repo', '-r', help='Github repository name')
@click.option('--path', '-p', help='Github repository file path')
@click.option('--name', '-n', help='Want to upload asset name')
@click.option('--config', '-c', help='Specified other config file',
        type=click.Path(exists=True))
@click.option('--release', '-R', help='Github repository release name, If give it means upload a release asset.')
@click.option('--yes', '-y', is_flag = True, default = False, help = 'All questions answered yes')
#  @click.argument('filepath', type=click.Path(exists=True))
@click.argument('filepath')
def run(filepath, path, repo, yes, release, name, config):
    '''
    Github Object Storage System
    '''

    kw = locals()
    #  print(kw)
    create(**kw)
    pass

if __name__ == "__main__":
    run()
