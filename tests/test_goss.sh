#!/usr/bin/env bash
# Author: wxnacy(wxnacy@gmail.com)
# Description:

PYFILE=goss/app/upload_file.py

get_status() {
    echo `curl $1 -IsL -w "%{http_code}" -o /dev/null`
}

generate_path() {
    echo test/`date '+%s'`
}

testCreateFile() {
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

testUploadAsset() {
    name=$(date '+%s')
    URL=https://raw.githubusercontent.com/wxnacy/goss/master/tests/mac.png
    python ${PYFILE} -r test -R v1.0.0 -n $name tests/mac.png
    url="https://github.com/wxnacy/test/releases/download/v1.0.0/$name"
    echo $url
    code=$(get_status $url)
    assertEquals $code 403
}

. /usr/local/Cellar/shunit2/2.1.7/bin/shunit2
