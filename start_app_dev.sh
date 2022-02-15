#!/bin/zsh

. venv/bin/activate
export FLASK_APP=emailsender
export FLASK_ENV=development
flask run
