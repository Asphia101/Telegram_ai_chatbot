#!/usr/bin/env bash
# fail on error
set -o errexit

# Upgrade pip, setuptools, wheel
pip install --upgrade pip setuptools wheel

# Install project dependencies
pip install -r requirements.txt
