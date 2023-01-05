#!/usr/bin/env python3

import re

pattern = re.compile('Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')
sensors = []

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
    
def blocked_in_row(row):
    blocked = set()
    for s in sensors:
        res = blocked_by_sensor(s['sx'], s['sy'], s['d'], row)
        if res == None:
            continue
        (left, right) = res
        for x in range(left, right+1):
            blocked.add(x)
    return len(blocked)

def beacons_in_row(row):
    beaconxs = set()
    for s in sensors:
        bx, by = s['bx'], s['by']
        if by == row:
            beaconxs.add(bx)
    return len(beaconxs)

def main():
#    parse_file('test.txt')
    parse_file('input.txt')
#    row = 10
    row = 2000000
    print(blocked_in_row(row) - beacons_in_row(row))

if __name__ == '__main__':
    main()
