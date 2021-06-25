#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
for github
"""
import requests
from .exceptions import GitException



class Git(object):
    domain = None
    proxy = None
    proxies = {}

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        if self.proxy:
            self.proxies = {
                "http": self.proxy,
                "https": self.proxy,
            }

    @classmethod
    def _fmt_url(cls, path):
        if not cls.domain:
            raise GitException('git domain 不能为空')
        return 'https://{domain}{path}'.format(domain = cls.domain, path = path)

    @classmethod
    def _get(cls, path):
        url = cls._fmt_url(path)
        return cls._request('get', url, proxies = proxies)

    @classmethod
    def _request(cls, method, url, proxies=None):
        kw = {}
        if proxies and isinstance(proxies, dict):
            kw['proxies'] = proxies
        return requests.request(method, url, **kw)

