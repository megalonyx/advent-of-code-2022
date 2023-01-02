#!/usr/bin/env python3

snafu_digits = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
snafu_back = {0: '0', 1: '1', 2: '2', 3: '=', 4: '-'}

total = 0

def parse_line(line):
    global total
    dec = decimal_from_snafu(line)
    #print(line, dec)
    total += dec

def parse_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            parse_line(line.strip('\n'))

def decimal_from_snafu(snafu):
    dec = 0
    pos = 1
    while len(snafu) > 0:
        s = snafu[-1]
        snafu = snafu[:-1]
        digit = snafu_digits[s]
        dec += digit * pos
        pos *= 5
    return dec

def snafu_from_decimal(dec):
    snafu = ''
    carry = 0
    while dec > 0:
        div, rem = dec // 5 , dec % 5
        carry = 1 if rem >= 3 else 0
        digit = snafu_back[rem]
        snafu = digit + snafu
        dec = div + carry
    return snafu


def main():
#    parse_file('test.txt')
    parse_file('input.txt')
    print(snafu_from_decimal(total))

if __name__ == '__main__':
    main()
