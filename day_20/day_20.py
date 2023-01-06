#!/usr/bin/env python3

originals = []
positions = []
LEN = 0

def parse_line(line):
    global originals, positions
    originals.append(int(line))
    positions.append(len(originals) - 1)

def parse_file(filename):
    global LEN
    with open(filename, 'r') as f:
        for line in f:
            parse_line(line.strip('\n'))
    LEN = len(positions)

def move_in_array(arr, pos, newpos):
    val = arr[pos]
    lefthalf = arr[:pos]
    righthalf = arr[pos+1:]
    spliced = lefthalf + righthalf
    newarr = spliced[:newpos] + [val] + spliced[newpos:]
    return newarr

def move_number(n):
    global originals, positions
    pos = positions.index(n)
    val = originals[pos]
    if val == 0:
        return
    newpos = normalize_pos(pos + val)
    originals = move_in_array(originals, pos, newpos)
    positions = move_in_array(positions, pos, newpos)

def normalize_pos(potentialpos):
    newpos = potentialpos
    if newpos <= 0:
        newpos = newpos + LEN - 1
    elif newpos >= LEN:
        newpos = newpos - LEN + 1
    if newpos < 0 or newpos > LEN - 1:
        tmppos = newpos
        newpos = newpos % LEN - 1
    return newpos

def grove_number():
    pos = originals.index(0)
    return originals[(pos+1000) % LEN] + originals[(pos+2000) % LEN] + \
        originals[(pos+3000) % LEN]

def main():
#    parse_file('test.txt')
    parse_file('input.txt')
    for i in range(LEN):
        move_number(i)
    print(grove_number())

if __name__ == '__main__':
    main()
