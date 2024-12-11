#!/usr/bin/env python3

def load_input(filename):
    e = []
    with open(filename) as f:
        for line in f:
            (a, b) = line.strip().split(':')
            e.append((int(a), list(map(int, b.strip().split()))))
    return e


def concat(a, b):
    return int(str(a) + str(b))


def eval_rec(partial, operands, idx, with_concat):
    nxt = operands[idx]
    if idx == len(operands) - 1:
        yield partial + nxt
        yield partial * nxt
        if with_concat:
            yield concat(partial, nxt)
    else:
        yield from eval_rec(partial + nxt, operands, idx + 1, with_concat)
        yield from eval_rec(partial * nxt, operands, idx + 1, with_concat)
        if with_concat:
            yield from eval_rec(concat(partial, nxt), operands, idx + 1, with_concat)


def eval(operands, with_concat):
    p = operands[0]
    if len(operands) == 1:
        yield p
    else:
        yield from eval_rec(p, operands, 1, with_concat)


def sum_correct(equations, with_concat=False):
    total = 0
    for (result, operands) in equations:
        for candidate in eval(operands, with_concat):
            if candidate == result:
                total += result
                break
    return total


equations = load_input('input.txt')

print('AOC 2024 07 part 1')
print(sum_correct(equations))

print()

print('AOC 2024 07 part 2')
print(sum_correct(equations, with_concat=True))
