from class_book import Book
from class_library import Library
from class_user import User, Librarian
from getpass import getpass
from generate_id import (
    generate_book_id,
    generate_user_id,
    generate_librarian_id
)


def main():
    library = Library()
    library_start()


def library_start():
    while True:
        print("Welcome to the Library!")
        print("1 - Log in")
        print("2 - Create a new user account")
        print("3 - Create a new librarian account")