#!/usr/bin/env python3

robot = ['+++   +++',
         '+++***+++',
         '++*****++',
         ' ******* ',
         ' ******* ',
         ' ******* ',
         '++*****++',
         '+++***+++',
         '+++   +++']

with open('kart.txt') as f:
#with open('mini.txt') as f:
    kart = [line for line in f.read().split('\n') if line]

kart_h = len(kart)
kart_w = len(kart[0])

robot_h = len(robot)
robot_w = len(robot[0])

cleaned = [list(line) for line in kart]

print(kart_h, kart_w, robot_h, robot_w)

def check_robot(i, j):
    for x in range(1, robot_h - 1):
        for y in range(1, robot_w - 1):
            if robot[x][y] == '*' and kart[i + x][j + y] == 'x':
                return False
    return True

def clean(i, j):
    global cleaned
    for x in range(max(0, -i), min(robot_h, kart_h - i)):
        for y in range(max(0, -j), min(robot_w, kart_w - j)):
            if robot[x][y] == '*':
                cleaned[i + x][j + y] = 's'
            elif robot[x][y] == '+' and cleaned[i + x][j + y] == ' ':
                cleaned[i + x][j + y] = '.'

for i in range(-1, kart_h - robot_h + 2):
    #print(f'line {i}')
    for j in range(-1, kart_w - robot_w + 2):
        if check_robot(i, j):
            clean(i, j)

#with open('cleaned.txt', 'w') as f:
#    for l in cleaned:
#        f.write(''.join(l) + '\n')
print(sum([l.count(' ') for l in cleaned]))

