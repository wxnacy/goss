#!/usr/bin/env bash
# Author: wxnacy(wxnacy@gmail.com)
# Description:

PYFILE=goss/app/upload_file.py

get_status() {
    ws http code $1
    # echo `curl $1 -IsL -w "%{http_code}" -o /dev/null`
    # `curl $1 -IsL -w "%{http_code}\n" -o /dev/null`
}

generate_path() {
    echo test/`date '+%s'`
}

testCreateFileWithConfig() {
    python ${PYFILE} tests/mac.png -c tests/config -y
    url="https://raw.githubusercontent.com/wxnacy/test/master/config_test/mac.png"
    code=$(get_status $url)
    assertEquals $code 200
}

testCreateFile() {
    path=$(generate_path)
    python ${PYFILE} -r test tests/mac.png -y
    url="https://raw.githubusercontent.com/wxnacy/test/master/mac.png"
    code=$(get_status $url)
    assertEquals $code 200
}

testCreateFileWithPath() {
    path=$(generate_path)
    python ${PYFILE} -r test -p $path tests/mac.png
    url="https://raw.githubusercontent.com/wxnacy/test/master/${path}"
    code=$(get_status $url)
    assertEquals $code 200
}

testCreateByUrl() {
    path=$(generate_path)
    URL=https://raw.githubusercontent.com/wxnacy/goss/master/tests/mac.png
    python ${PYFILE} -r test -p $path $URL
    url="https://raw.githubusercontent.com/wxnacy/test/master/${path}"
    code=$(get_status $url)
    assertEquals $code 200
}

. /usr/local/Cellar/shunit2/2.1.7/bin/shunit2
