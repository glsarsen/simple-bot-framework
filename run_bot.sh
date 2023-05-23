#!/usr/bin/env bash

source venv/bin/activate
waitress-serve --listen=127.0.0.1:30000 wsgi:app