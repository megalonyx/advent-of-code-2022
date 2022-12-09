#!/usr/bin/env python3

moves = []
tail_positions = set( [ (0,0) ] )

head_x = 0
head_y = 0
tail_x = 0
tail_y = 0

def parse_line(line):
    global moves
    data = line.split(' ')
    direction = data[0]
    if direction == 'U':
        delta = (0, -1)
    elif direction == 'D':
        delta = (0, 1)
    elif direction == 'L':
        delta = (-1, 0)
    elif direction == 'R':
        delta = (1, 0)
    else:
        print('error')
        exit
    num = int(data[1])
    moves.append( (delta, num) )

def parse_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            parse_line(line.strip('\n'))

def head_and_tail_are_touching():
    dx = head_x - tail_x
    dy = head_y - tail_y
    return abs(dx) <= 1 and abs(dy) <= 1

def move_head(dx, dy):
    global head_x, head_y
    head_x += dx
    head_y += dy

def sign(x):
    if x > 0:
        return +1
    elif x < 0:
        return -1
    else:
        return 0
    
def clamp(d):
    return min(abs(d), 1) * sign(d)

def move_tail():
    global tail_x, tail_y, tail_positions
    dx = head_x - tail_x
    dy = head_y - tail_y
    if dx == 0 and abs(dy) == 2:        # directly up or down
        tail_y += clamp(dy)
    elif abs(dx) == 2 and dy == 0:      # directly right or left
        tail_x += clamp(dx)
    else:                               # diagonally
        tail_x += clamp(dx)
        tail_y += clamp(dy)
    tail_positions.add( (tail_x, tail_y) )

def all_moves():
    for (delta, num) in moves:
        for i in range(num):
            move_head(delta[0], delta[1])
            if not head_and_tail_are_touching():
                move_tail()
        
def main():
#    parse_file('test.txt')
    parse_file('input.txt')
    all_moves()
    print(len(tail_positions))

if __name__ == '__main__':
    main()
