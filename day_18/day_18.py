#!/usr/bin/env python3

cubeposs = []
sidestouched = []
possiblesides = [
        (-1, 0, 0),
        (1, 0, 0),
        (0, -1, 0),
        (0, 1, 0),
        (0, 0, -1),
        (0, 0, 1)
        ]

def add(a, b):
    ax, ay, az = a
    bx, by, bz = b
    return (ax+bx, ay+by, az+bz)

def test_connected(i, j):
    for s in possiblesides:
        if add(cubeposs[i], s) == cubeposs[j]:
            sidestouched[i].add(s)
        if add(cubeposs[j], s) == cubeposs[i]:
            sidestouched[j].add(s)
    
def test_all_cubes():
    for i in range(len(cubeposs)):
        for j in range(i+1, len(cubeposs)):
            test_connected(i, j)

def free_surfaces():
    total = 0
    for i in range(len(sidestouched)):
        total += (6 - len(sidestouched[i]))
    return total

def parse_line(line):
    global cubeposs, sidestouched
    coords = tuple([int(c) for c in line.split(',')])
    cubeposs.append(coords)
    sidestouched.append(set())

def parse_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            parse_line(line.strip('\n'))

def main():
#    parse_file('test.txt')
    parse_file('input.txt')
    test_all_cubes()
    print(free_surfaces())

if __name__ == '__main__':
    main()
