#!/bin/sh
set -e 
cd /github/workspace

pip install -r requirements.txt
pip install .

ls -l 

sc --sarif "$1"