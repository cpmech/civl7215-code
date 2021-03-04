#!/bin/bash

set -e

files=`find . -iname "*.py"`

for file in $files; do
    echo
    echo
    echo "=== $file ================================="
    python3 $file
done
