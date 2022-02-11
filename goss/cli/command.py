#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""
import sys
import os

from csarg import CommandArgumentParserFactory

from goss.argument.command import CmdArgumentParser
from goss.loggers import get_logger
from goss.cli.run_mode import RUN_MODE

from goss.utils import get_current_module_path
from goss.utils import load_module

logger = get_logger('main')

__all__ = ['Command']

class Command(object):
    logger = get_logger('Command')

    def __init__(self, *args, **kwargs):
        # 动态加载参数解析器模板
        argument_dir = os.path.join(get_current_module_path(), 'argument')
        for name in os.listdir(argument_dir):
            if not name.endswith('.py'):
                continue
            module = f'goss.argument.{name[:-3]}'
            load_module(module)

    def convert_argparse(self, cmd):
        """转换参数解析器"""
        for clz in CmdArgumentParser.__subclasses__():
            if clz.cmd == cmd:
                return clz.default()

        return CommandArgumentParserFactory.build_parser(cmd)

    #  @profile
    def run(self):
        RUN_MODE.set_command()

        sys_args = sys.argv[1:]
        if not sys_args:
            sys_args = ['shell']
        cmd = sys_args[0]

        args_text = ' '.join(sys_args)

        # 转换参数解析器
        parser = self.convert_argparse(cmd)
        #  args = parser.parse_args(args_text)

        parser.run(args_text)


def main():
    Command().run()

