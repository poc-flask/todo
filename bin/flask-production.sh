#!/usr/bin/env bash

gunicorn -w $NUM_OF_WORKERS -b 0.0.0.0:5000 manage:app
