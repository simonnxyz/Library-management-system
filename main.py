from class_book import Book
from class_library import Library
from class_user import User, Librarian
from getpass import getpass
from generate_id import (
    generate_book_id,
    generate_user_id,
    generate_librarian_id
)
from errors import (
    WrongPasswordError,
)

library = Library()
user = None
librarian = None


def main():
    print('Welcome to the Library!')
    library_start()


def start_menu():
    print('1 - Log in')
    print('2 - Create a new user account')
    print('3 - Create a new librarian account')
    print('4 - Exit')


def library_start():
    start_menu()
    while True:
        choice = int(input('Enter your choice: '))
        if choice == 1:
            login()
        elif choice == 2:
            pass
        elif choice == 3:
            pass
        elif choice == 4:
            print("Thank you for using the Library. " +
                  "We hope to see you again soon!")
            break
        else:
            print('Wrong number, try again.')


def login():
    global user, librarian
    while True:
        try:
            id = input('Enter your ID: ')
            password = getpass('Enter your password: ')
            check = library.login_role_check(id, password)
            if check:
                if str(check.get("id")).startswith('1'):
                    librarian = Librarian(**check)
                    librarian_menu()
                else:
                    user = User(**check)
                    user_menu()
            else:
                print("User with the given ID not found.")
                raise WrongPasswordError
        except WrongPasswordError as e:
            print(e)
            answer = input('Do you want to try again? [y/n] ')
            if answer == 'y':
                pass
            else:
                start_menu()
                break


def librarian_menu():
    print('librarian')


def user_menu():
    print('user')


if __name__ == "__main__":
    main()
