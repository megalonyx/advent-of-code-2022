#!/usr/bin/env python3

import numpy as np
import skimage.morphology as sm

cubes = []
maxx = 0
minx = 100
maxy = 0
miny = 100
maxz = 0
minz = 100

NOTHING = 0
LAVA = 1
FILLVAL = 2

def parse_line(line):
    global cubes, maxx, minx, maxy, miny, maxz, minz
    coords = tuple([int(c) for c in line.split(',')])
    cubes.append(coords)
    x, y, z = coords
    maxx = max(maxx, x)
    minx = min(minx, x)
    maxy = max(maxy, y)
    miny = min(miny, y)
    maxz = max(maxz, z)
    minz = min(minz, z)

def parse_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            parse_line(line.strip('\n'))

def create_and_populate_grid():
    global minx, miny, minz, maxx, maxy, maxz
    if minx < 0 or miny < 0 or minz < 0:
        print('error')
        exit(1)
    minx = 0
    miny = 0
    minz = 0
    maxx += 1
    maxy += 1
    maxz += 1
    grid = np.zeros( (maxx+1, maxy+1, maxz+1), dtype=np.uint8)
    for c in cubes:
        x, y, z = c
        grid[x, y, z] = LAVA
    return grid

def flood_fill(grid):
    start = (0, 0, 0)
    if grid[start] != 0:
        print('error')
        exit(1)
    return sm.flood_fill(grid, start, FILLVAL, connectivity=1)

def count_val_neighbouring(grid, coord, val):
    x, y, z = coord
    total = 0
    if x-1 >= minx:
        if grid[ x-1, y, z ] == val: total += 1
    else:
        total += 1
    if x+1 <= maxx:
        if grid[ x+1, y, z ] == val: total += 1
    else:
        total += 1
    if y-1 >= miny:
        if grid[ x, y-1, z ] == val: total += 1
    else:
        total += 1
    if y+1 <= maxy:
        if grid[ x, y+1, z ] == val: total += 1
    else:
        total += 1
    if z-1 >= minz:
        if grid[ x, y, z-1 ] == val: total += 1
    else:
        total += 1
    if z+1 <= maxz:
        if grid[ x, y, z+1 ] == val: total += 1
    else:
        total += 1
    return total

def count_surface(grid):
    total = 0
    it = np.nditer(grid, flags=['multi_index'])
    for c in it:
        if c == LAVA:
            total += count_val_neighbouring(grid, it.multi_index, FILLVAL)
    return total

def count(grid, val):
    total = 0
    for c in np.nditer(grid):
        if c == val:
            total += 1
    return total

def count_neighbours(grid, val_central, val_neighbour):
    total = 0
    it = np.nditer(grid, flags=['multi_index'])
    for c in it:
        if c == val_central:
            total += count_val_neighbouring(grid, it.multi_index,  val_neighbour)
    return total

def main():
#    parse_file('test.txt')
    parse_file('input.txt')
    grid = create_and_populate_grid()
    grid = flood_fill(grid)
    print(count_surface(grid))

if __name__ == '__main__':
    main()
