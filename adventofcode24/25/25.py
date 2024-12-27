#!/usr/bin/env python3

def load_input(filename):
    keys = []
    locks = []
    trans = str.maketrans(".#", "01")
    with open(filename) as f:
        temp = []
        for line in f:
            line = line.strip()
            if len(line) == 0:
                process_template(temp, keys, locks)
                temp = []
                continue
            temp.append(int(line.translate(trans), 16))
        process_template(temp, keys, locks)
    return (keys, locks)


def process_template(temp, keys, locks):
    if temp[0] == 0x11111:
        locks.append(sum(temp[1:]))
    elif temp[-1] == 0x11111:
        keys.append(sum(temp[:-1]))
    else:
        raise Error('invalid template')


def check_key(key, lock):
    m = key + lock
    return m & 0xf0000 <= 0x50000 and m & 0xf000 <= 0x5000 and m & 0xf00 <= 0x500 and m & 0xf0 <= 0x50 and m & 0xf <= 0x5


def check_keys(keys, locks):
    pairs = 0
    for k in keys:
        for l in locks:
            #print(hex(k), hex(l), check_key(k, l))
            if check_key(k, l):
                pairs += 1
    return pairs


(keys, locks) = load_input('input.txt')
#(keys, locks) = load_input('test.txt')


print('AOC 2024 25 part 1')
print(check_keys(keys, locks))

print()

print('AOC 2024 25 part 2')
#print(system.total_complexity(codes, 25))



