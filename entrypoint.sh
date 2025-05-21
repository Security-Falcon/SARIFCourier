#!/bin/sh
pip install -r requirements.txt
pip install .
sc --sarif "$1"