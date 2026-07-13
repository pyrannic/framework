#!/usr/bin/env bash

# Script to build and upload the package.

rm -rf dist/*
python3 -m build
python3 -m twine upload dist/* --verbose  
