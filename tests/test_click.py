#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

import click


# 30  40  黑色
# 31  41  红色
# 32  42  绿色
# 33  43  黄色
# 34  44  蓝色
# 35  45  紫红色
# 36  46  青蓝色
# 37  47  白色

if __name__ == "__main__":

    print("\n {}[{};{};{}m{}{}[0m\n\n".format(0x1B, 0, 0, 30, "testPrintColor", 0x1B))
    for fg in (
            'black',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white'
            ):
        click.secho(fg, fg=fg)
