#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
for github
"""
import requests
from .git import Git

proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

class Github(Git):
    domain = 'api.github.com'

    @classmethod
    def profile(cls):
        #  url = 'https://api.github.com/repos/octocat/hello-world/community/profile'
        path = '/repos/{}/{}/community/profile'.format('wxnacy', 'goss')

        return cls._get(path)

if __name__ == "__main__":
    #  g = Git()
    #  g._fmt_url('test')
    g = Github()
    res = g.profile()
    print(res.json())

