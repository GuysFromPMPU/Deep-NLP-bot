#!/bin/bash

export FLASK_APP=main.py
export FLASK_DEBUG=0
export FLASK_ENV=production
flask run --host="::" --cert cert.pem --key key.pem --with-threads
