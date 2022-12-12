#!/usr/bin/env python3

def parse_line(line):
    pass

def parse_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            parse_line(line.strip('\n'))

def main():
    parse_file('test.txt')
#    parse_file('input.txt')

if __name__ == '__main__':
    main()
