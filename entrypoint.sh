#!/bin/sh
cp /app/requirements.txt .
cp /app/setup.py .
cp /app/main.py .
cp /app/sarif-schema-2.1.0.json .

pip install -r requirements.txt
pip install .
sc --sarif "$1"