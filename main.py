from class_book import Book
from class_library import Library
from class_user import User, Librarian
from getpass import getpass
from generate_id import (
    generate_book_id,
    generate_user_id,
    generate_librarian_id
)
from options_lists import (
    print_with_box,
    print_with_box_down,
    print_with_box_up,
    start_options,
    user_options,
    librarian_options,
)
from errors import (
    WrongPasswordError,
    WrongIDError,
    EmptyNameError,
    EmptyPasswordError,
    ShortPasswordError,
)

library = Library()
user = None
librarian = None


def main():
    print_with_box_up(' Welcome to the Library! ', 27)
    library_start()


def library_start():
    start_options()
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
            create_account()
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
                    librarian_options()
                else:
                    user = User(**check)
                    user_options()
            else:
                raise WrongIDError
        except (WrongPasswordError, WrongIDError) as e:
            print(e)
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                start_options()
                break
        except ValueError:
            print('Incorrect ID.')
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                start_options()
                break


def create_account():
    global user
    while True:
        try:
            name = input('Enter your name: ')
            password = getpass('Enter your password: ')
            user = User(generate_user_id(), name, password)
            library.add_new_user(user)
            user_options()
        except (EmptyNameError, EmptyPasswordError, ShortPasswordError) as e:
            print(e)
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                start_options()
                break


if __name__ == "__main__":
    main()
