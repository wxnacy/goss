#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

from flask import Flask
from flask import request

from wush import run
from goss.constants import Constants
from goss.config import save_github_access_token

app = Flask(__name__)


@app.route('/github/callback')
def github_callback():
    args = request.args
    code = args.get("code")
    res = run('www_github', 'oauth_access_token',
        params={ "code": code },
        config = Constants.CONFIG_PATH)
    access_token = res.get("access_token")
    save_github_access_token(access_token)
    return res

@app.route('/github/test')
def test():
    return {}

def run_server():
    app.run(port = 3000, debug=True)

if __name__ == "__main__":
    run_server()
