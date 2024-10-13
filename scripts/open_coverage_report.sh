#!/usr/bin/env bash
set -e

original_dir=$PWD

echo "Unzipping /tmp/act-artifacts/1"

# 'unzip -o' == overwrite
cd /tmp/act-artifacts/1/htmlcov
unzip -o htmlcov
firefox index.html

cd $original_dir
