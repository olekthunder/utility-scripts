#!/bin/bash

git diff -U0 "$1" -- '*.py' | flake8 --diff --show-source

