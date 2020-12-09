#!/bin/bash

cat numbers.txt | sed -e 's/,/\n/g' | sort -n | awk '$1 - prev == 2 { print prev + 1 } { prev = $1 }'
