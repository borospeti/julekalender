#!/usr/bin/env python3


def run(filename):
    orker = 10
    besokt = 0
    with open(filename) as f:
        for line in f.readlines():
            for food in line.strip():
                if food == '1':
                    orker += 2
                besokt += 1
                orker -= 1
                if orker == 0:
                    return besokt

#print(run('mini.txt'))
print(run('rute.txt'))

