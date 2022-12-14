#!/usr/bin/env python3

from collections import deque

raw_data = []
heightmap = []
size_x = 0
size_y = 0
start_x = 0
start_y = 0
end_x = 0
end_y = 0
visited = set()
distances = []
myq = deque()
solutions = []

def parse_line(line):
    global raw_data
    raw_data.append(line)

def parse_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            parse_line(line.strip('\n'))

def init_distances():
    global distances
    leny = len(raw_data)
    lenx = len(raw_data[0])
    maxval = lenx * leny
    distances = [ [maxval for _ in range(leny)] for _ in range(lenx)]

def build_heightmap():
    global heightmap, size_x, size_y, start_x, start_y, end_x, end_y, lowest_solution
    size_y = len(raw_data)
    size_x = len(raw_data[0])
    heightmap = [ [0 for _ in range(size_y)] for _ in range(size_x)]  # transposed to raw_data
    for y in range(size_y):
        for x in range(size_x):
            c = raw_data[y][x]
            if c == 'S':
                start_x = x
                start_y = y
                heightmap[x][y] = ord('a') - ord('a')
            elif c == 'E':
                end_x = x
                end_y = y
                heightmap[x][y] = ord('z') - ord('a')
            elif 'a' <= c <= 'z':
                heightmap[x][y] = ord(c) - ord('a')
            else:
                print('error')
                exit
    lowest_solution = size_x * size_y
                
def print_heightmap():
    for y in range(size_y):
        for x in range(size_x):
            print(chr(heightmap[x][y]+ord('a')), end='')
        print()

def print_distances():
    for y in range(size_y):
        for x in range(size_x):
            print(chr(distances[x][y]+ord('a')), end='')
        print()

def neighbours(point):
    x, y = point
    ns = []
    for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if 0 <= x + dx < size_x and \
           0 <= y + dy < size_y:
               if heightmap[x+dx][y+dy] >= heightmap[x][y] - 1:
                   ns.append( (x+dx, y+dy) )
    return ns

def search():
    global myq, visited, distances
    p = myq.popleft()
    x, y = p
    dist = distances[x][y]
    if heightmap[x][y] == 0:
        solutions.append(dist)
#    print(dist)
    visited.add(p)
    for n in neighbours(p):
        if not n in visited:
            x, y = n
            if distances[x][y] > dist + 1:
                distances[x][y] = dist + 1
                myq.append( n )

def main():
    global myq
#    parse_file('test.txt')
    parse_file('input.txt')
    build_heightmap()
    init_distances()
#    print_heightmap()
    distances[end_x][end_y] = 0
    myq.append( (end_x, end_y) )
    while len(myq) > 0:
        search()
    print(sorted(solutions)[0])

if __name__ == '__main__':
    main()
