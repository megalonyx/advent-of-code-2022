#!/usr/bin/env python3

monkeys = []

def parse_line(line):
    global monkeys
    last = len(monkeys)-1
    if line.startswith('Monkey'):
        monkeys.append({})
        monkeys[last+1]['numinspected'] = 0
    elif line.startswith('  Starting'):
        stuff = line.split(' ')
        splitted = stuff[4:]
        items = [int(s.strip(',')) for s in splitted]
        monkeys[last]['items'] = items
    elif line.startswith('  Operation:'):
        stuff = line.split(' ')
        splitted = stuff[6:]
        operator = splitted[0]
        value = splitted[1]
        if value == 'old':
            op = (operator, value)
        else:
            op = (operator, int(value))
        monkeys[last]['operation'] = op
    elif line.startswith('  Test:'):
        stuff = line.split(' ')
        splitted = stuff[3:]
        monkeys[last]['divisor'] = int(splitted[2])
    elif line.startswith('    If true:'):
        stuff = line.split(' ')
        splitted = stuff[6:]
        monkeys[last]['iftrue'] = int(splitted[3])
    elif line.startswith('    If false:'):
        stuff = line.split(' ')
        splitted = stuff[6:]
        monkeys[last]['iffalse'] = int(splitted[3])
    elif line == '':
        pass
    else:
        print('error')
        exit

def parse_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            parse_line(line.strip('\n'))

def worry(level, op):
    if op[1] == 'old':
        if op[0] == '+':
            return level + level
        elif op[0] == '*':
            return level * level
        else:
            print('error')
            exit
    else:
        if op[0] == '+':
            return level + op[1]
        elif op[0] == '*':
            return level * op[1]
        else:
            print('error')
            exit

def inspect_item():
    pass

def monkey_turn(i):
    global monkeys
    items = monkeys[i]['items']
    monkeys[i]['items'] = []
    for it in items:
        monkeys[i]['numinspected'] += 1
        print('  Monkey inspects an item with a worry level of',it,'.')
        newworry = worry(it, monkeys[i]['operation'])
        print('    New worry level is', newworry)
        newworry = int(newworry / 3)
        print('    Monkey gets bored with item. Worry level is divided by 3 to ', newworry)
        divisor = monkeys[i]['divisor']
        if newworry % divisor == 0:
            print('    Current worry level is divisible by',divisor)
            newmonkey = monkeys[i]['iftrue']
        else:
            print('    Current worry level is not divisible by', divisor)
            newmonkey = monkeys[i]['iffalse']
        monkeys[newmonkey]['items'].append(newworry)
        print('    Item with worry level ', newworry, 'is thrown to monkey',newmonkey)

def full_round():
    for i in range(len(monkeys)):
        print('Monkey',i)
        monkey_turn(i)

def print_monkeys():
    for i in range(len(monkeys)):
        print('Monkey',i,':',end='')
        for it in monkeys[i]['items']:
            print(it,',',end='')
        print()

def print_monkey_inspections():
    for i in range(len(monkeys)):
        print('Monkey',i,'inspected items:',monkeys[i]['numinspected'],'times.')

def extract_monkey_inspections():
    insps = []
    for m in monkeys:
        insps.append(m['numinspected'])
    return insps

def main():
#    parse_file('test.txt')
    parse_file('input.txt')
#    for m in monkeys:
#        print(m)
#        print()
    for _ in range(20):
        full_round()
#    print_monkey_inspections()
    res = sorted(extract_monkey_inspections())[-2:]
    print(res[0]*res[1])

if __name__ == '__main__':
    main()
