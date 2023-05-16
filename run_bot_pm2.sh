#!/usr/bin/env bash

source venv/bin/activate
gunicorn -w 2 wsgi:app --log-file bot.log -b 127.0.0.1:30000