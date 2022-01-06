#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""

from goss import utils


def test_format_repo_pathes():

    filepath = 'tests/test_utils.py'
    pathes = ['test_utils.py']
    assert utils.format_repo_pathes(filepath) == pathes

    filepath = 'tests/test_utils.py'
    path = 'test.py'
    pathes = ['test.py']
    assert utils.format_repo_pathes(filepath, path) == pathes

    filepath = 'tests/test_utils.py'
    path = 'test/'
    pathes = ['test/test_utils.py']
    assert utils.format_repo_pathes(filepath, path) == pathes

    filepath = 'goss/resources/config'
    path = 'test/'
    pathes = ['test/config/config.yml',
        'test/config/module/api_github.yml',
        'test/config/module/www_github.yml',
        ]
    _pathes = utils.format_repo_pathes(filepath, path)
    assert _pathes == pathes

    filepath = 'goss/resources/config'
    path = 'test'
    pathes = ['test/config/config.yml',
        'test/config/module/api_github.yml',
        'test/config/module/www_github.yml',
        ]
    _pathes = utils.format_repo_pathes(filepath, path)
    assert _pathes == pathes

    filepath = 'goss/resources/config'
    path = ''
    pathes = ['config/config.yml',
        'config/module/api_github.yml',
        'config/module/www_github.yml',
        ]
    _pathes = utils.format_repo_pathes(filepath, path)
    assert _pathes == pathes
