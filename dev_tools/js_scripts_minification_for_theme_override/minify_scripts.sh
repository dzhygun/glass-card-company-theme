#!/bin/bash

if ! command -v terser &> /dev/null
then
    echo "terser not found, installing globally..."
    npm install -g terser
fi

terser scripts.js -o scripts.min.js -c -m
