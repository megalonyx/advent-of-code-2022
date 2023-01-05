#!/usr/bin/env python3

import re

pattern = re.compile('Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')
sensors = []
MINX = 0
MAXX = 4000000
MINY = 0
MAXY = 4000000

def dist(ax, ay, bx, by):
    return abs(ax - bx) + abs(ay - by)

def parse_line(line):
    global sensors
    m = pattern.match(line)
    sx = int(m.group(1))
    sy = int(m.group(2))
    bx = int(m.group(3))
    by = int(m.group(4))
    d = dist(sx, sy, bx, by)
    sens = {'sx': sx,
            'sy': sy,
            'bx': bx,
            'by': by,
            'd':  d}
    sensors.append(sens)

def parse_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            parse_line(line.strip('\n'))

def blocked_by_sensor(sx, sy, d, row):
    vertical_dist = abs(sy - row)
    rest_dist = d - vertical_dist
    if rest_dist < 0:
        return None
    mid = sx
    left = mid - rest_dist
    right = mid + rest_dist
    return (left, right)
    
def find_in_row(row):
    blocked = []
    for s in sensors:
        res = blocked_by_sensor(s['sx'], s['sy'], s['d'], row)
        if res == None:
            continue
        blocked.append(res)
    return unify(blocked)

def unify(intervals):
    news = intervals[:]
    wasjoined = True
    while wasjoined:
        wasjoined = False
        olds = news
        news = []
        totest = olds[0]
        for i in range(1, len(olds)):
            if is_disjunct(totest, olds[i]):
                news.append(olds[i])
            else:
                totest = join(totest, olds[i])
                wasjoined = True
        news.append(totest)
    return news

def join(a, b):
    return ( min(a[0], b[0]), max(a[1], b[1]) )

def is_disjunct(a, b):
    return a[1]+1 < b[0] or b[1]+1 < a[0]

def find_overall():
    for row in range(MINY, MAXY+1):
        res = find_in_row(row)
        if (len(res)) > 1:
            hole = get_hole(res[0], res[1])
            return tuning_frequency( (hole, row) )

def get_hole(a, b):
    if a[1] < b[0]:
        return a[1] + 1
    elif b[1] < a[0]:
        return b[1] + 1
    else:
        print('error')
        exit(1)

def tuning_frequency(b):
    return b[0] * 4000000 + b[1]

def main():
#    parse_file('test.txt')
    parse_file('input.txt')
    print(find_overall())

if __name__ == '__main__':
    main()
