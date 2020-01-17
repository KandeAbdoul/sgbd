#!/bin/bash
. venv/bin/activate
python3 serverRest.py
sleep 5
curl http://0.0.0.0:8888/ 