#!/bin/sh
gunicorn -w 10 serve:app
