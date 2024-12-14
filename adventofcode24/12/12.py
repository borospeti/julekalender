#!/usr/bin/env python3

def load_input(filename):
    garden = []
    with open(filename) as f:
        for line in f:
            garden.append(line.strip())
    return garden


def is_perimeter


garden = load_input('input.txt')

print('AOC 2024 08 part 1')
print(len(locate_antinodes(antennas, height, width)))

print()

print('AOC 2024 08 part 2')
print(len(locate_antinodes(antennas, height, width, full_grid=True)))

