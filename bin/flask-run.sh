#!/usr/bin/env bash
cd src
FLASK_APP=manage:app flask run -h 0.0.0.0
