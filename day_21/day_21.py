#!/usr/bin/env python3

monkeys = dict()

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mul(a, b):
    return a * b

def div(a, b):
    return int(a / b)

def parse_line(line):
    global monkeys
    monkey, rest = line.split(':')
    ops = rest[1:].split(' ')
    if len(ops) == 1:
        monkeys[monkey] = int(ops[0])
    else:
        op = ops[1]
        v1 = ops[0]
        v2 = ops[2]
        if op == '+':
            op = add
        elif op == '-':
            op = sub
        elif op == '*':
            op = mul
        elif op == '/':
            op = div
        else:
            print('error')
            exit()
        if str.isdigit(v1):
            v1 = int(v1)
        if str.isdigit(v2):
            v2 = int(v2)
        monkeys[monkey] = [op, v1, v2]

def parse_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            parse_line(line.strip('\n'))

def replace(monk, val):
    global monkeys
    for key in monkeys:
        if isinstance(monkeys[key], list):
            if monkeys[key][1] == monk:
                monkeys[key][1] = val
                #print('match', monk)
                #print(monkeys[key])
            if monkeys[key][2] == monk:
                monkeys[key][2] = val
                #print('match', monk)
                #print(monkeys[key])
            if isinstance(monkeys[key][1], int) and isinstance(monkeys[key][2], int):
                monkeys[key] = monkeys[key][0](monkeys[key][1], monkeys[key][2])
                #print('replacing', key, 'by', monkeys[key])

def iterate():
    global monkeys
    while isinstance(monkeys['root'], list):
        for key in monkeys:
            if isinstance(monkeys[key], int):
                if key == 'root':
                    print(monkeys[key])
                    exit
                #print('replacing', key, 'with', monkeys[key])
                replace(key, monkeys[key])

def main():
#    parse_file('test.txt')
    parse_file('input.txt')
    iterate()
    print(monkeys['root'])

if __name__ == '__main__':
    main()
