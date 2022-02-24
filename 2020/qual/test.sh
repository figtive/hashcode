#!/bin/bash

for FILENAME in $(find . -name '*.in'); do
    CASE=${FILENAME:2:-3}
    echo "$CASE"
    time python3 solver.py < "$CASE.in" 2> "$CASE.out"
done
