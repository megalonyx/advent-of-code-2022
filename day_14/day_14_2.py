#!/usr/bin/env python3

sand_origin = (500, 0)
rock_paths = []
AIR = 0
ROCK = 1
SAND = 2
minx = sand_origin[0]
maxx = sand_origin[0]
miny = sand_origin[1]
maxy = sand_origin[1]
cave = []

def parse_line(line):
    global rock_paths
    pointstrings = line.split(' -> ')
    points = []
    for s in pointstrings:
        sx, sy = s.split(',')
        points.append( (int(sx), int(sy) ) )
    for i in range(len(points)-1):
        rock_paths.append( ( points[i], points[i+1] ) )

def parse_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            parse_line(line.strip('\n'))

def cave_read(point):
    px = point[0]
    py = point[1]
    if px < minx or px > maxx or py < miny or py > maxy:
        return AIR
    x = px - minx
    y = py - miny
    return cave[x][y]

def cave_write(point, val):
    x = point[0] - minx
    y = point[1] - miny
    cave[x][y] = val

def build_rock_path(rp):
    p1, p2 = rp
    distx = p2[0] - p1[0]
    disty = p2[1] - p1[1]
    dx = min(1, abs(distx))
    dy = min(1, abs(disty))
    if distx < 0:
        dx = -dx
    if disty < 0:
        dy = -dy
    x, y = p1
    cave_write(p1, ROCK)
    cave_write(p2, ROCK)
    while (x, y) != p2:
        x += dx
        y += dy
        cave_write( (x, y), ROCK)
    
def build_cave():
    global minx, maxx, miny, maxy, cave
    for rp in rock_paths:
        minx = min(minx, rp[0][0])
        minx = min(minx, rp[1][0])
        maxx = max(maxx, rp[0][0])
        maxx = max(maxx, rp[1][0])
        miny = min(miny, rp[0][1])
        miny = min(miny, rp[1][1])
        maxy = max(maxy, rp[0][1])
        maxy = max(maxy, rp[1][1])
    # add bottom:
    maxy += 2
    # make sure cave is wide enough:
    minx = min(minx, 500 - maxy - 5)   # -5 as safety margin
    maxx = max(maxx, 500 + maxy + 5)   # +5 as safety margin
    sizex = maxx - minx + 1
    sizey = maxy - miny + 1
    cave = [ [AIR for _ in range(sizey)] for _ in range(sizex)]
    for rp in rock_paths:
        build_rock_path(rp)
    build_rock_path( ( (minx, maxy), (maxx, maxy) ) )

def print_cave():
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            t = cave_read( (x, y) )
            if t == AIR:
                c = '.'
            elif t == ROCK:
                c = '#'
            elif t == SAND:
                c = 'o'
            else:
                print('error')
                exit
            print(c, end='')
        print()

def drop_sand(p):
    while True:
        x, y = p
        if x < minx or x > maxx or y > maxy:
            return False   # escape
        if cave_read( (x, y+1) ) == AIR:
            p = (x, y+1)
            continue
        elif cave_read( (x-1, y+1) ) == AIR:
            p = (x-1, y+1)
            continue
        elif cave_read( (x+1, y+1) ) == AIR:
            p = (x+1, y+1)
            continue
        else: # comes to rest
            cave_write(p, SAND)
            if p == sand_origin:
                return False
            return True

def main():
#    parse_file('test.txt')
    parse_file('input.txt')
    build_cave()
    i = 0
    while drop_sand(sand_origin):
        i += 1
    print_cave()
    print(i+1)

if __name__ == '__main__':
    main()
