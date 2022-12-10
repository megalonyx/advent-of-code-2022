#!/usr/bin/env python3

program = []
X = 1
cycle = 1
signals = []

def parse_line(line):
    global program
    split = line.split(' ')
    cmd = split[0]
    val = None
    if len(split) > 1:
        val = int(split[1])
    program.append( (cmd, val) )

def parse_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            parse_line(line.strip('\n'))

def test_signal_strength():
    global signals
    if ((cycle - 20) % 40) == 0:
        print(X * cycle)
        signals.append(X * cycle)

def execute_noop():
    global cycle
    test_signal_strength()
    cycle += 1

def execute_addx(val):
    global cycle, X
    test_signal_strength()
    cycle += 1
    test_signal_strength()
    cycle += 1
    X += val

def execute_instruction(cmd, optval):
    if cmd == 'addx':
        execute_addx(optval)
    elif cmd == 'noop':
        execute_noop()
    else:
        print('error')
        exit

def execute_program():
    for i in range(len(program)):
        execute_instruction(program[i][0], program[i][1])
    
def main():
#    parse_file('test.txt')
    parse_file('input.txt')
    execute_program()
    print(sum(signals[0:6]))

if __name__ == '__main__':
    main()
