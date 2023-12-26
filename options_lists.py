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


def start_list():
    print_with_box('1 -> Log in', 27)
    print_with_box_down('2 -> Create a new account', 27)
    print_with_box_down('3 -> Exit', 27)


def user_list():
    print_with_box('1 -> Available books', 27)
    print_with_box_down('3 -> Check your books', 27)
    print_with_box_down('4 -> Check stats', 27)
    print_with_box_down('6 -> Borrow a book', 27)
    print_with_box_down('7 -> Return a book', 27)
    print_with_box_down('8 -> Use extension', 27)
    print_with_box_down('9 -> Reserve a book', 27)
    print_with_box_down('10 -> Cancel reservation', 27)
    print_with_box_down('11 -> Log out', 27)


def librarian_list():
    print('librarian')
