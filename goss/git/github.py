#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
for github
"""
import requests

from wapi import Wapi

from goss.git import Git
from goss.common import constants

#  proxies = {
    #  "http": "http://127.0.0.1:7890",
    #  "https": "http://127.0.0.1:7890",
#  }

class Github(Git):
    domain = 'api.github.com'

    def __init__(self, owner, repo=None, *args, **kwargs):
        self._owner = owner
        self._repo = repo
        self.www_wapi = Wapi(module_name = 'www_github',
            config_root=constants.WAPI_CONFIG_ROOT)
        self.api_wapi = Wapi(module_name = 'api_github',
            config_root=constants.WAPI_CONFIG_ROOT)
        self.api_wapi.config.get_env().add( owner=self._owner )

    def repo_profile(self, repo=None):
        if repo:
            self._repo = repo
        self.api_wapi.config.get_env().add( repo=self._repo )
        return self.api_wapi.request('repo_profile')

    def repo_content(self, repo, path):
        if repo:
            self._repo = repo
        self.api_wapi.config.get_env().add(
            repo=self._repo,
            path = path)
        return self.api_wapi.request('repo_content')

if __name__ == "__main__":
    g = Github('wxnacy')
    #  res = g.repo_profile('goss')
    res = g.repo_content('book', '2014.md')
    import json
    print(json.dumps(res.json(), indent=4))

