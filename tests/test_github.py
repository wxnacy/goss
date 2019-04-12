#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

import unittest
import configparser
from goss.github import Github
from goss.app import utils

cred = configparser.ConfigParser()
cred.read(utils.GOSS_CREDENTIAL_PATH)
default = cred['default']
g = Github(default['user'], default['password'])
g.set_owner(default['owner'])

conf = configparser.ConfigParser()
conf.read(utils.GOSS_CONFIG_PATH)
author = conf['user']
g.set_author(author['name'], author['email'])


class TestMain(unittest.TestCase):
    repo = 'test100'
    file_sha = 'c26a11aaedfcad82b539003c77e81e9df6862f3c'
    path = 'test.png'

    def setUp(self):
        '''before each test function'''
        pass

    def tearDown(self):
        '''after each test function'''
        pass

    def test_create_repository(self):
        code, data = g.create_repository(self.repo)
        self.assertEqual(code, 201)

        code, data = g.get_repository(g.owner, self.repo)
        self.assertEqual(code, 200)

    def test_upload(self):
        code, data = g.create_from_file(g.owner, self.repo, 'mac.png',
                self.path)
        self.assertEqual(code, 201)
        code, data = g.create_from_file(g.owner, self.repo, 'mac.png',
                self.path)
        self.assertEqual(code, 422)

    def test_get(self):
        code, data = g.get_file(g.owner, self.repo, self.path)
        self.assertEqual(code, 200)
        self.assertEqual(data.get('sha'), self.file_sha)

    def test_delete_file(self):
        code, data = g.delete_file(g.owner, self.repo, self.path, self.file_sha)
        self.assertEqual(code, 200)

    def test_delete_repo(self):
        code, data = g.delete_repository(g.owner, self.repo)
        self.assertEqual(code, 204)


if __name__ == "__main__":
    unittest.main()
