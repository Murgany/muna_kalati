#!/bin/bash

python manange.py collectstatic && gunicorn --workers 2 config.wsgi