#!/usr/bin/env python3

import os


def load_input(filename):
    files = []
    with open(filename) as f:
        disk = f.read().strip()
        file_id = 0
        space = False
        for c in disk:
            blocks = int(c)
            if space:
                files.append((None, blocks))
            else:
                files.append((file_id, blocks))
                file_id += 1
            space = not space
    return files


def f_id(f):
    return f[0]

def f_size(f):
    return f[1]

def is_file(f):
    return f_id(f) is not None

def is_space(f):
    return f_id(f) is None


def compact_disk(files):
    free = 0
    left = 0
    right = len(files) - 1
    work_file = None
    work_space = None
    while left <= right:
        if work_space is None and is_file(files[left]):
            yield files[left]
            left += 1
            continue
        if work_file is None and is_space(files[right]):
            free += f_size(files[right])
            right -= 1
            continue
        if work_space is None:
            work_space = files[left]
            left += 1
        if work_file is None:
            work_file = files[right]
            right -= 1
        rem = f_size(work_space) - f_size(work_file)
        if rem >= 0:
            yield work_file
            free += f_size(work_file)
            work_file = None
            work_space = (None, rem) if rem > 0 else None
        else:
            yield (f_id(work_file), f_size(work_space))
            work_file = (f_id(work_file), -rem)
            work_space = None
    if work_file is not None:
        yield work_file
    if work_space is not None:
        free += f_size(work_space)
    yield (None, free)

def compute_checksum(files):
    sector = 0
    checksum = 0
    for (i, l) in files:
        if i is not None:
            checksum += (i * (sector + sector + l - 1) * l) // 2
        sector += l
    return checksum


files = load_input('input.txt')

print('AOC 2024 09 part 1')
print(compute_checksum(compact_disk(files)))

print()

print('AOC 2024 09 part 2')
os.system('dotnet script 9-2.cs');


