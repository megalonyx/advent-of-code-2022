#!/usr/bin/env python3

NUM_OF_NODES = 10
moves = []
visited = [ set( [ (0,0) ] ) for _ in range(NUM_OF_NODES) ]
node_pos = [(0,0)] * NUM_OF_NODES
# node_pos[0]: head; node_pos[NUM_OF_NODES-1]: tail

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

def nodes_are_touching(n1, n2):
    dx = node_pos[n1][0] - node_pos[n2][0]
    dy = node_pos[n1][1] - node_pos[n2][1]
    return abs(dx) <= 1 and abs(dy) <= 1

def move_head(dx, dy):
    global node_pos
    head_x = node_pos[0][0]
    head_y = node_pos[0][1]
    head_x += dx
    head_y += dy
    node_pos[0] = (head_x, head_y)

def sign(x):
    if x > 0:
        return +1
    elif x < 0:
        return -1
    else:
        return 0
    
def clamp(d):
    return min(abs(d), 1) * sign(d)

def move_tail(n):
    global node_pos, visited
    head_x = node_pos[n-1][0]
    head_y = node_pos[n-1][1]
    tail_x = node_pos[n][0]
    tail_y = node_pos[n][1]
    dx = head_x - tail_x
    dy = head_y - tail_y
    if dx == 0 and abs(dy) == 2:        # directly up or down
       tail_y  += clamp(dy)
    elif abs(dx) == 2 and dy == 0:      # directly right or left
        tail_x += clamp(dx)
    else:                               # diagonally
        tail_x += clamp(dx)
        tail_y += clamp(dy)
    node_pos[n] = (tail_x, tail_y)
    visited[n].add( (tail_x, tail_y) )

def move_all_tails():
    for n in range(1, NUM_OF_NODES):
        if not nodes_are_touching(n-1, n):
            move_tail(n)
    
def all_moves():
    for (delta, num) in moves:
        for i in range(num):
            move_head(delta[0], delta[1])
            move_all_tails()
        
def main():
#    parse_file('test.txt')
#    parse_file('test2.txt')
    parse_file('input.txt')
    all_moves()
    print(len(visited[NUM_OF_NODES-1]))

if __name__ == '__main__':
    main()
