#!/usr/local/bin/python3

lineno = 0
lines = []
cwd = []
dircontents = {}
dirs = {}
total_dir_size = {}

def cd(path):
    global lineno, cwd
    if path == '/':
        cwd = []
    elif path == '..':
        cwd.pop()
    else:
        cwd.append(path)
    dirs[tuple(cwd)] = 1
    lineno += 1

def ls():
    global lineno, dircontents
    while lineno+1 < len(lines):    # avoid ls as last command with no output
        lineno += 1
        fields = lines[lineno].split(' ')
        if fields[0] == '$':
            return
        elif fields[0] == 'dir':
            pass
        else:
            size = int(fields[0])
            file = fields[1]
            add_file_to_dir(cwd, file, size)
    lineno += 1

def add_file_to_dir(dirlist, filename, size):
    global dircontents
    key = tuple(dirlist)
    value = (filename, size)
    if not key in dircontents:
        dircontents[key] = []
        dircontents[key].append(value)
    else:
        # avoid counting files more than once
        contents = dircontents[key]
        if not value in contents:
            dircontents[key].append(value)

def command(line):
    global lineno
    #skip '$ ':
    cli = line[2:]
    args = cli.split(' ')
    if args[0] == 'cd':
        cd(args[1])
    elif args[0] == 'ls':
        ls()
    else:
        print('error, unknown command')
        exit

def parse(line):
    global lineno
    if line[0] == '$':
        command(line)
    else:
        print('error, not a command')

def parse_all():
    global lineno
    lineno = 0
    while lineno < len(lines):
        parse(lines[lineno])

def calc_total_dir_sizes():
    global total_dir_size
    for key in dircontents:
        for f in dircontents[key]:
            add_size_to_dir_and_parents(key, f[1])

def add_size_to_dir_and_parents(key, size):
    global total_dir_size
    # add to original dir:
    if not key in total_dir_size:
        total_dir_size[key] = 0
    total_dir_size[key] += size
    dirlist = list(key)
    while len(dirlist) > 0:
        dirlist.pop()
        key = tuple(dirlist)
        if not key in total_dir_size:
            total_dir_size[key] = 0
        total_dir_size[key] += size

def first_task():
    total = 0
    for key in total_dir_size:
        size = total_dir_size[key]
        if size <= 100000:
            total += size
    return total

def second_task():
    unused_space = 70000000 - total_dir_size[()]
    target_space = 30000000
    needed_space = target_space - unused_space
    candidate = total_dir_size[()]
    for key in total_dir_size:
        size = total_dir_size[key]
        if size >= needed_space:
            candidate = min(candidate, size)
    return candidate

def main():
#    with open('test.txt') as f:
    with open('input.txt') as f:
        for line in f:
            lines.append(line.strip())
    parse_all()
    calc_total_dir_sizes()
    print('first: ', first_task())
    print('second: ', second_task())

if __name__ == '__main__':
    main()
