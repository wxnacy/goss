#!/usr/bin/env bash
# Author: wxnacy(wxnacy@gmail.com)
# Description:

for name in pyperclip wush loguru
do
    pt add $name
done

for name in pytest sphinx
do
    pt add -D $name
done
