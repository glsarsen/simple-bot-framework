#!/usr/bin/env bash

source venv/bin/activate
nohup gunicorn -w 2 wsgi:app --log-file bot.log -b 127.0.0.1:30000 &

sleep 10s
python3.9 viber_webhook.py