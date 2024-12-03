#!/bin/bash

cat input.txt | awk 'BEGIN { x=0; y=0; } { switch ($1) { case "forward": x=x+$2; break; case "down": y=y+$2; break; case "up": y=y-$2; break; } } END { print x, y, x*y; }'

cat input.txt | awk 'BEGIN { x=0; y=0; aim=0; } { switch ($1) { case "forward": x=x+$2; y=y+(aim*$2); break; case "down": aim=aim+$2; break; case "up": aim=aim-$2; break; } } END { print x, y, aim, x*y; }'
