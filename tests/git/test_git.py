#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""
import pytest

from goss.git import Git
from goss.git import Github
from goss.git.exceptions import GitException


def test_fmt_url():
    g = Git()

    with pytest.raises(GitException) as excinfo:
        g._fmt_url('/test')

    gh = Github()
    assert gh._fmt_url('/test'), 'https://{}/test'.format(gh.domain)
