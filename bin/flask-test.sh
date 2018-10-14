#!/usr/bin/env bash
coverage run --source src -m pytest --ignore migrations -W module
coverage report