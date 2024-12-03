#!/bin/bash

cat input.txt | awk 'BEGIN { a=999999; count=0; } { if ($1>a) count=count+1; a=$1; } END { print count; }'

cat input.txt | awk 'BEGIN { a=999999; b=999999; c=999999; sum=count=0; } { if (b+c+$1>a+b+c) count=count+1; a=b; b=c; c=$1; } END { print count; }'
