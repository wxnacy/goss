#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

from gos import __version__

from setuptools import setup, find_packages

setup(
    name = 'gos',
    version = __version__.__version__,
    keywords='python3',
    description = 'a library for python Developer',
    license = 'MIT License',
    url = 'https://github.com/wxnacy/gos',
    author = 'wxnacy',
    author_email = 'wxnacy@gmail.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [
        'click>=7.0',
        'pyperclip>=1.7.0',
        'requests>=2.21.0'
    ],
    entry_points={
        'console_scripts': ['gos=gos.app.upload_file:run'],
    },
    #  scripts=['bin/wpytool']
)

