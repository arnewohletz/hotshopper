#!/bin/bash

COMMAND=$1

if [ $COMMAND = "verify-pip-tools" ]; then
    pip-compile --version > /dev/null 2>&1
    if [ ! $? -eq 0 ]; then
         echo "pip-tools not found. Install via: pip install pip-tools"
         exit 1
    fi
fi