from print_methods import (
    print_with_box,
    print_with_box_down
)


def start_options():
    print_with_box('1 -> Log in', 27)
    print_with_box_down('2 -> Create a new account', 27)
    print_with_box_down('3 -> Exit', 27)


def user_options():
    print_with_box('1 -> Available books', 23)
    print_with_box_down('2 -> Search a book', 23)
    print_with_box_down('3 -> Check your books', 23)
    print_with_box_down('4 -> Check stats', 23)
    print_with_box_down('5 -> Log out', 23)


def filters_list():
    print_with_box('1 -> Keyword', 19)
    print_with_box_down('2 -> Genre', 19)
    print_with_box_down('3 -> Author', 19)
    print_with_box_down('4 -> Release year', 19)
    print_with_box_down('5 -> Go Back', 19)


def library_books_options():
    print_with_box('1 -> Borrow a book', 21)
    print_with_box_down('2 -> Reserve a book', 21)
    print_with_box_down('3 -> Go back', 21)


def users_books_options():
    print_with_box('1 -> Return a book', 25)
    print_with_box_down('2 -> Use extension', 25)
    print_with_box_down('3 -> Cancel reservation', 25)
    print_with_box_down('4 -> Go back', 25)


def librarian_options():
    print_with_box('1 -> Library books', 31)
    print_with_box_down('2 -> Search a book', 31)
    print_with_box_down('3 -> Library users/librarians', 31)
    print_with_box_down('4 -> Search a user/librarian', 31)
    print_with_box_down('5 -> Check stats', 31)
    print_with_box_down('6 -> Log out', 31)


def librarians_books_options():
    print_with_box('1 -> Add a new book', 25)
    print_with_box_down('2 -> Add a copy of book', 25)
    print_with_box_down('3 -> Remove the book', 25)
    print_with_box_down('4 -> Go back', 25)


def librarians_users_options():
    print_with_box('1 -> Add a new user', 27)
    print_with_box_down('2 -> Add a new librarian', 27)
    print_with_box_down('3 -> Remove the user', 27)
    print_with_box_down('4 -> Remove the librarian', 27)
    print_with_box_down('5 -> Go back', 27)


def stats_options():
    print_with_box('1 -> Books stats', 18)
    print_with_box_down('2 -> Users stats', 18)
    print_with_box_down('3 -> Go back', 18)
