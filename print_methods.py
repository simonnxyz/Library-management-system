def print_with_box(message, length):
    print(f'+{"-"*length}+')
    print(f'| {message}' + ' '*(length-len(message)-1) + '|')
    print(f'+{"-"*length}+')


def print_with_box_up(message, length):
    print(f'+{"-"*length}+')
    print(f'| {message}' + ' '*(length-len(message)-1) + '|')


def print_with_box_down(message, length):
    print(f'| {message}' + ' '*(length-len(message)-1) + '|')
    print(f'+{"-"*length}+')


def red(message):
    return ('\033[91m' + message + '\033[0m')


def green(message):
    return ('\033[92m' + message + '\033[0m')


def bold(message):
    return ('\033[1m' + message + '\033[0m')
