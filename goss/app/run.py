#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

import click
from goss import Github
from goss import __version__
from goss.app import utils
from goss.app.logger import Logger
import configparser
import os
import pyperclip
import json

GOSS_CONFIG_HOME = '{}/.config/goss'.format(os.getenv("HOME"))
GOSS_CONFIG_PATH = '{}/config'.format(GOSS_CONFIG_HOME)
GOSS_CREDENTIAL_PATH = '{}/credentials'.format(GOSS_CONFIG_HOME)
GOSS_USER_INFO_PATH = '{}/user.json'.format(GOSS_CONFIG_HOME)

logger = Logger()

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__.__version__)
    ctx.exit()

@click.group()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
@click.pass_context
def run(ctx):
    '''
    Github Object Storage
    '''
    if not os.path.exists(GOSS_CONFIG_HOME):
        os.mkdir(GOSS_CONFIG_HOME)
    if os.path.exists(GOSS_CREDENTIAL_PATH):
        cred = configparser.ConfigParser()
        cred.read(GOSS_CREDENTIAL_PATH)
        secs = cred.sections()
        if 'default' in secs:
            default_cred = cred['default']
            user = default_cred['user']
            password = default_cred['password']
            ctx.obj = Github(user, password)

def init_credentials_path():
    if not os.path.exists(GOSS_CONFIG_HOME):
        os.mkdir(GOSS_CONFIG_HOME)

    #  if not os.path.exists(GOSS_CREDENTIAL_PATH):
        #  with open(GOSS_CREDENTIAL_PATH, '+w') as f:
            #  f.flush()
            #  f.close()


@run.command(help='Log in to the github account')
@click.option('--user', '-u', prompt='Your Github user', help = 'Your Github user')
@click.option('--password', '-p', prompt='Your Github password',
        help = 'Your Github password',hide_input=True)
@click.option('--yes', '-y', is_flag = True, default = False, help = 'All questions answered yes')
@click.pass_context
def login(ctx, user, password, yes):
    g = ctx.obj
    confirm = utils.make_error_msg('The login information already exists. Do you want to replace it?')
    if not yes:
        if g and not click.confirm(confirm):
            return
    conf = configparser.ConfigParser()
    conf['default'] = dict(user = user, password = password)

    g = Github(user, password)
    code, data = g.get_user_info()
    if code != 200:
        utils.print_failed()
        logger.error('用户名或密码错误')
        return

    owner = data.get("name")
    conf['default']['owner'] = owner
    with open(GOSS_CREDENTIAL_PATH, 'w') as f:
        conf.write(f)
    with open(GOSS_USER_INFO_PATH, 'w') as f:
        f.write(json.dumps(data, indent = 4))
        f.flush()
        f.close()

    conf_data = dict(name = owner)
    email = data.get("email")
    if email:
        conf_data['email'] = email

    utils.config(GOSS_CONFIG_PATH, 'user', **conf_data)

    utils.print_success()
    logger.info('Name  :', owner)
    logger.info('Email :', email)


@run.command()
@click.option('--repo', '-r', is_flag = True, help = 'To create repository')
@click.option('--name', '-n', required = True, help = 'Create object name')
@click.option('--orga', '-o', help = 'If want create organization repository. Is required')
@click.pass_context
def create(ctx, repo, name, orga):
    g = ctx.obj
    if not g:
        click.echo('You have not logged in yet, please go to goss-cli login to login')
        click.echo('You have not logged in yet, please go to goss-cli login to login')
        click.echo('You have not logged in yet, please go to goss-cli login to login')
        ctx.exit()

    if repo:
        click.echo('Begin create repository')
        click.echo('{}\t: https://github.com/{}/{}'.format(
            utils.make_progress_msg('Url'), name, name))
        click.secho('Waiting...', fg='yellow')
        if orga:
            flag, data = g.create_organization_repository(orga, name)
        else:
            flag, data = g.create_repository(name)
        if not flag:
            utils.print_error(data['message'])
            for err in data['errors']:
                utils.print_error('\t' + err['message'])
        else:
            utils.print_success()

@run.command()
@click.argument('name', required = False)
@click.argument('value', required = False)
@click.pass_context
def config(ctx, name, value):
    if name and value and '.' in name:
        names = name.split('.')
        section = names[0]
        key = names[1]
        utils.config(GOSS_CONFIG_PATH, section, **{key: value})
        utils.print_success()
        return

    conf = configparser.ConfigParser()
    conf.read(GOSS_CONFIG_PATH)
    secs = conf.sections()
    for sec in secs:
        click.echo('[{}]'.format(sec))
        kv = conf[sec]
        for k, v in kv.items():
            click.echo('    {} = {}'.format(k, v))

    pass

if __name__ == "__main__":
    run()
    #  credentials()
