#!/bin/zsh

for FILENAME in $(find . -name '*.in' | sort); do
    CASE=${FILENAME:2:-3}
    echo "$CASE"
    time python solver.py < "$CASE.in" 2> "$CASE.out"
done
