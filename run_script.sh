#!/bin/bash
python3 -m venv ./venv \
 && source ./venv/bin/activate \
 && ./venv/bin/pip3 install --log ./pip.log -r requirements.txt \
 && python3 $1 \
 && deactivate