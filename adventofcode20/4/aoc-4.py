#!/usr/bin/env python3

import re
import sys

ALL_KEYS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'}
REQ_KEYS = ALL_KEYS - {'cid'}

FIELD_DATA_REGEX = {'byr' : r'\d{4}',
                    'iyr' : r'\d{4}',
                    'eyr' : r'\d{4}',
                    'hgt' : r'(\d+)(cm|in)',
                    'hcl' : r'#[a-f0-9]{6}',
                    'ecl' : r'amb|blu|brn|gry|grn|hzl|oth',
                    'pid' : r'\d{9}',
                    'cid' : r'.*'}


def check_field(k, v):
    m = re.fullmatch(FIELD_DATA_REGEX[k], v)
    if not m:
        return False
    if k == 'byr':
        return 1920 <= int(v) <= 2002
    elif k == 'iyr':
        return 2010 <= int(v) <= 2020
    elif k == 'eyr':
        return 2020 <= int(v) <= 2030
    elif k == 'hgt':
        if m.group(2) == 'cm':
            return 150 <= int(m.group(1)) <= 193
        else:  # 'in'
            return 59 <= int(m.group(1)) <= 76
    return True


def check_passport(p, check_fields=False):
    if not p:
        return None
    if p.keys() - ALL_KEYS:
        print('unknown key in', p)
    if REQ_KEYS - p.keys():
        return False
    if not check_fields:
        return True
    for k,v in p.items():
        if not check_field(k, v):
            return False
    return True


def check_passports(check_fields=False):
    valid = 0
    with open('input.txt') as f:
        passport = {}
        for line in f.readlines():
            fields = line.split()
            if not fields:
                if check_passport(passport, check_fields=check_fields):
                    valid += 1
                passport = {}
                continue
            for f in fields:
                k, v = f.split(':')
                passport[k] = v
        if check_passport(passport, check_fields=check_fields):
            valid += 1
    return valid


print('part 1')
print(f'valid:{check_passports()}')

print('part 2')
print(f'valid:{check_passports(check_fields=True)}')



