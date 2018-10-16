#!/usr/bin/env bash
cd src
DEBUG=True FLASK_APP=manage:app flask run -h 0.0.0.0