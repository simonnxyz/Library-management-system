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
    WrongIDError,
)

library = Library()
user = None
librarian = None


def main():
    print_with_box(' Welcome to the Library! ', 27)
    library_start()


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


def start_menu():
    print_with_box_down('1 -> Log in', 27)
    print_with_box_down('2 -> Create a new account', 27)
    print_with_box_down('3 -> Exit', 27)


def library_start():
    start_menu()
    while True:
        for _ in range(3):
            try:
                choice = int(input('Enter your choice: '))
                break
            except ValueError:
                print('Invalid input, please enter a number.')
        else:
            message = ('You have exceeded the maximum number ' +
                       'of attempts. Please try again later.')
            print_with_box(message, len(message) + 2)
            quit()
        if choice == 1:
            login()
        elif choice == 2:
            pass
        elif choice == 3:
            message = ("Thank you for using our Library. " +
                       "We hope to see you again soon!")
            print_with_box(message, len(message) + 2)
            quit()
        else:
            print('Wrong number, try again.')


def login():
    global user, librarian
    while True:
        try:
            id = int(input('Enter your ID: '))
            password = getpass('Enter your password: ')
            check = library.login_role_check(id, password)
            if check:
                if str(check["id"]).startswith('1'):
                    librarian = Librarian(**check)
                    librarian_menu()
                else:
                    user = User(**check)
                    user_menu()
            else:
                raise WrongIDError
        except (WrongPasswordError, WrongIDError) as e:
            print(e)
            answer = input('Do you want to try again? [y/n] ')
            if answer != 'y':
                start_menu()
                break
        except ValueError:
            print('Incorrect ID.')
            answer = input('Do you want to try again? [y/n] ')
            if answer != 'y':
                start_menu()
                break


def create_account():
    global user


def librarian_menu():
    print('librarian')


def user_menu():
    print('user')


if __name__ == "__main__":
    main()
