#!/usr/bin/env bash

cd src
FLASK_APP=manage:app flask db upgrade -d migrations
