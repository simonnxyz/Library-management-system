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
    filters_list,
    user_book_options,
    users_books_options,
    librarian_options,
)
from errors import (
    WrongPasswordError,
    WrongIDError,
    EmptyNameError,
    EmptyPasswordError,
    ShortPasswordError,
    UsersBookError,
    BorrowedBookError,
    NoBookIDError,
    NoBookOwnerError,
    NoKeywordError,
    KeywordNotFoundError,
    GenresNotFoundError,
    UnavailableGenreError,
    YearsNotFoundError,
    UnavailableYearError,
    AuthorsNotFoundError,
    UnavailableAuthorError,
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
                    raise ValueError
            except ValueError:
                print('Invalid input, try again.')
        else:
            message = ('You have exceeded the maximum number ' +
                       'of attempts. Please try again later.')
            print_with_box(message, len(message) + 2)
            quit()


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
                    user_interface()
            else:
                raise WrongIDError
        except (WrongPasswordError, WrongIDError) as e:
            print(e)
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                library_start()
        except ValueError:
            print('Incorrect ID.')
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                library_start()


def create_account():
    global user
    while True:
        try:
            name = input('Enter your name: ')
            password = getpass('Enter your password: ')
            user = User(generate_user_id(), name, password)
            library.add_new_user(user)
            user_interface()
        except (EmptyNameError, EmptyPasswordError, ShortPasswordError) as e:
            print(e)
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                library_start()


def user_interface():
    while True:
        user_options()
        for _ in range(3):
            try:
                choice = int(input('Enter your choice: '))
                if choice == 1:
                    print(library.available_books_info())
                    book_options_interface()
                elif choice == 2:
                    search_book_interface()
                elif choice == 3:
                    pass
                elif choice == 4:
                    pass
                elif choice == 5:
                    library_start()
                else:
                    raise ValueError
            except ValueError:
                print('Invalid input, try again.')
        else:
            message = ('You have exceeded the maximum number ' +
                       'of attempts. Please try again later.')
            print_with_box(message, len(message) + 2)
            quit()
        break


def search_book_interface():
    filters_list()
    while True:
        for _ in range(3):
            try:
                choice = int(input('Enter your choice: '))
                if choice == 1:
                    search_keyword()
                    book_options_interface()
                elif choice == 2:
                    try:
                        print('\n'.join(library.available_genres()))
                        search_genre()
                        book_options_interface()
                    except GenresNotFoundError as e:
                        print(e)
                        answer = input('Do you want to try again? [y/n] ')
                        if answer.lower() != 'y':
                            user_interface()
                        else:
                            search_book_interface()
                elif choice == 3:
                    try:
                        print('\n'.join(library.available_authors()))
                        search_author()
                        book_options_interface()
                    except AuthorsNotFoundError as e:
                        print(e)
                        answer = input('Do you want to try again? [y/n] ')
                        if answer.lower() != 'y':
                            user_interface()
                        else:
                            search_book_interface()
                elif choice == 4:
                    try:
                        print('\n'.join(library.available_years()))
                        search_year()
                        book_options_interface()
                    except YearsNotFoundError as e:
                        print(e)
                        answer = input('Do you want to try again? [y/n] ')
                        if answer.lower() != 'y':
                            user_interface()
                        else:
                            search_book_interface()
                elif choice == 5:
                    user_interface()
                else:
                    raise ValueError
            except ValueError:
                print('Invalid input, try again.')
        else:
            message = ('You have exceeded the maximum number ' +
                       'of attempts. Please try again later.')
            print_with_box(message, len(message) + 2)
            quit()


def search_keyword():
    global library
    while True:
        try:
            keyword = input('Enter the keyword: ')
            print(library.search_book_by_keyword(keyword))
            break
        except (NoKeywordError, KeywordNotFoundError) as e:
            print(e)
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                search_book_interface()
        except ValueError:
            print('Incorrect ID.')
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                search_book_interface()


def search_genre():
    global library
    while True:
        try:
            genre = input('Enter the genre: ')
            print(library.search_book_by_genre(genre))
            break
        except UnavailableGenreError as e:
            print(e)
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                search_book_interface()
        except ValueError:
            print('Incorrect ID.')
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                search_book_interface()


def search_author():
    global library
    while True:
        try:
            author = input('Enter the author: ')
            print(library.search_book_by_author(author))
            break
        except UnavailableAuthorError as e:
            print(e)
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                search_book_interface()
        except ValueError:
            print('Incorrect ID.')
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                search_book_interface()


def search_year():
    global library
    while True:
        try:
            year = input('Enter the year: ')
            print(library.search_book_by_year(year))
            break
        except UnavailableYearError as e:
            print(e)
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                search_book_interface()
        except ValueError:
            print('Incorrect ID.')
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                search_book_interface()


def book_options_interface():
    user_book_options()
    while True:
        for _ in range(3):
            try:
                choice = int(input('Enter your choice: '))
                if choice == 1:
                    borrow_book()
                elif choice == 2:
                    reserve_book()
                elif choice == 3:
                    user_interface()
                else:
                    raise ValueError
            except ValueError:
                print('Invalid input, try again.')
        else:
            message = ('You have exceeded the maximum number ' +
                       'of attempts. Please try again later.')
            print_with_box(message, len(message) + 2)
            quit()


def borrow_book():
    global user
    while True:
        try:
            id = int(input('Enter book ID: '))
            user.borrow_book(id)
            library.update_data()
            user_interface()
        except (UsersBookError, BorrowedBookError, NoBookIDError) as e:
            print(e)
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                user_interface()
        except ValueError:
            print('Incorrect ID.')
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                user_interface()


def reserve_book():
    global user
    while True:
        try:
            id = int(input('Enter book ID: '))
            user.reserve_book(id)
            library.update_data()
            user_interface()
        except (UsersBookError, NoBookOwnerError, NoBookIDError) as e:
            print(e)
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                user_interface()
        except ValueError:
            print('Incorrect ID.')
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                user_interface()


def librarian_interface():
    librarian_options()


if __name__ == "__main__":
    main()
