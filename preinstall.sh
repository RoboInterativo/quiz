#!/bin/bash
mkdir venv 
python3 -m virtualenv -p python3 venv
. ./venv/bin/activate 
pip install -r requirements.txt
