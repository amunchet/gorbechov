#!/bin/sh
gunicorn -b 0.0.0.0:80 -w 10 serve:app
