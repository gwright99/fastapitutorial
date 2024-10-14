#!/usr/bin/env bash
set -e

original_dir=$PWD

echo "Unzipping /tmp/act-artifacts/1"

# 'unzip -o' == overwrite
# This won't work once I start suffixing reports based on python version. Replace with loop.
# cd /tmp/act-artifacts/1/htmlcov
# unzip -o htmlcov
# firefox index.html

versions="3.10.15 3.12.7"

for version in ${versions}
do
    cd /tmp/act-artifacts/1/htmlcov-${version}
    unzip -o htmlcov-${version}
    firefox index.html
    cd $original_dir
done

cd $original_dir
