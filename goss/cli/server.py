#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

from flask import Flask
from flask import request

from goss.config import save_github_access_token
from goss.models import Github

app = Flask(__name__)


@app.route('/github/callback')
def github_callback():
    args = request.args
    code = args.get("code")
    version = args.get("version")
    res = Github().oauth_access_token(code)
    data = res.json()
    access_token = data.get("access_token")
    save_github_access_token(version, access_token)
    return data

@app.route('/github/test')
def test():
    return {}

def run_server():
    app.run(port = 3000, debug=True)

if __name__ == "__main__":
    run_server()
