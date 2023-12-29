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
    library_books_options,
    users_books_options,
    librarian_options,
    librarians_books_options,
    librarians_users_options,
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
    NotUsersBookError,
    ReservedBookError,
    NotEnoughExtensionsError,
    UserWithBooksError,
    NoLibrarianIDError,
    EmptyTitleError,
    NoAuthorError,
    NoReleaseYearError,
    NoGenreError,
    RemoveYourselfError,
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
                    librarian_interface()
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
                    library_books_user_interface()
                elif choice == 2:
                    search_book_user_interface()
                elif choice == 3:
                    print(user.get_borrowed_books())
                    print(user.get_history())
                    print(user.get_reservations())
                    users_books_interface()
                elif choice == 4:
                    get_stats()
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


def search_book_user_interface():
    filters_list()
    while True:
        for _ in range(3):
            try:
                choice = int(input('Enter your choice: '))
                if choice == 1:
                    search_keyword(search_book_user_interface)
                    library_books_user_interface()
                elif choice == 2:
                    try:
                        print('\n'.join(library.available_genres()))
                        search_genre(search_book_user_interface)
                        library_books_user_interface()
                    except GenresNotFoundError as e:
                        print(e)
                        answer = input('Do you want to try again? [y/n] ')
                        if answer.lower() != 'y':
                            user_interface()
                        else:
                            search_book_user_interface()
                elif choice == 3:
                    try:
                        print('\n'.join(library.available_authors()))
                        search_author(search_book_user_interface)
                        library_books_user_interface()
                    except AuthorsNotFoundError as e:
                        print(e)
                        answer = input('Do you want to try again? [y/n] ')
                        if answer.lower() != 'y':
                            user_interface()
                        else:
                            search_book_user_interface()
                elif choice == 4:
                    try:
                        print('\n'.join(library.available_years()))
                        search_year(search_book_user_interface)
                        library_books_user_interface()
                    except YearsNotFoundError as e:
                        print(e)
                        answer = input('Do you want to try again? [y/n] ')
                        if answer.lower() != 'y':
                            user_interface()
                        else:
                            search_book_user_interface()
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


def search_by(option, errors, search_interface):
    while True:
        try:
            result = option()
            print(result)
            break
        except errors as e:
            print(e)
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                search_interface()
        except ValueError:
            print('Incorrect input.')
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                search_interface()


def search_keyword(search_interface):
    def keyword():
        global library
        keyword = input('Enter the keyword: ')
        return library.search_book_by_keyword(keyword)
    search_by(
        keyword,
        (NoKeywordError, KeywordNotFoundError),
        search_interface
    )


def search_genre(search_interface):
    def genre():
        global library
        genre = input('Enter the genre: ')
        return library.search_book_by_genre(genre)
    search_by(
        genre,
        UnavailableGenreError,
        search_interface
    )


def search_author(search_interface):
    def author():
        global library
        author = input('Enter the author: ')
        return library.search_book_by_author(author)
    search_by(
        author,
        UnavailableAuthorError,
        search_interface
    )


def search_year(search_interface):
    def year():
        global library
        year = input('Enter the year: ')
        return library.search_book_by_year(year)
    search_by(
        year,
        UnavailableYearError,
        search_interface
    )


def library_books_user_interface():
    library_books_options()
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


def user_operation(operation, errors, interface):
    global user
    while True:
        try:
            book_id = int(input('Enter book ID: '))
            operation(book_id)
            library.update_data()
            user_interface()
        except errors as e:
            print(e)
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                user_interface()
            else:
                interface()

        except ValueError:
            print('Incorrect ID.')
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                user_interface()
            else:
                interface()


def borrow_book():
    user_operation(
        user.borrow_book,
        (UsersBookError, BorrowedBookError, NoBookIDError),
        library_books_user_interface
    )


def reserve_book():
    user_operation(
        user.reserve_book,
        (UsersBookError, NoBookOwnerError, NoBookIDError),
        library_books_user_interface
    )


def users_books_interface():
    users_books_options()
    while True:
        for _ in range(3):
            try:
                choice = int(input('Enter your choice: '))
                if choice == 1:
                    return_book()
                elif choice == 2:
                    use_extension()
                elif choice == 3:
                    cancel_reservation()
                elif choice == 4:
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


def return_book():
    user_operation(
        user.return_book,
        (NotUsersBookError, NoBookIDError),
        users_books_interface
    )


def use_extension():
    user_operation(
        user.use_extension,
        (
            NotUsersBookError,
            ReservedBookError,
            NotEnoughExtensionsError,
            NoBookIDError
        ),
        users_books_interface
    )


def cancel_reservation():
    user_operation(
        user.cancel_reservation,
        (NotUsersBookError, NoBookIDError),
        users_books_interface
    )


def get_stats():
    pass


def librarian_interface():
    while True:
        librarian_options()
        for _ in range(3):
            try:
                choice = int(input('Enter your choice: '))
                if choice == 1:
                    print(library.available_books_info())
                    library_books_librarian_interface()
                elif choice == 2:
                    search_book_librarian_interface()
                elif choice == 3:
                    print(library.users_librarians())
                    library_users_librarian_interface()
                elif choice == 4:
                    pass
                elif choice == 5:
                    get_stats()
                elif choice == 6:
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


def library_books_librarian_interface():
    librarians_books_options()
    while True:
        for _ in range(3):
            try:
                choice = int(input('Enter your choice: '))
                if choice == 1:
                    add_book()
                elif choice == 2:
                    add_book_copy()
                elif choice == 3:
                    remove_book()
                elif choice == 4:
                    librarian_interface()
                else:
                    raise ValueError
            except ValueError:
                print('Invalid input, try again.')
        else:
            message = ('You have exceeded the maximum number ' +
                       'of attempts. Please try again later.')
            print_with_box(message, len(message) + 2)
            quit()


def librarian_id_operation(
        operation,
        errors,
        interface,
        obj_id,
        new_id=None,
        librarian_id=None
        ):
    global librarian
    while True:
        try:
            id = int(input(f'Enter {obj_id} ID: '))
            if new_id:
                operation(id, new_id)
            elif librarian_id:
                operation(id, librarian_id)
            else:
                operation(id)
            library.update_data()
            librarian_interface()
        except errors as e:
            print(e)
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                librarian_interface()
            else:
                interface()

        except ValueError:
            print('Incorrect ID.')
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                librarian_interface()
            else:
                interface()


def add_book():
    while True:
        try:
            title = input('Enter the title: ')
            author = input('Enter the author: ')
            release_year = input('Enter the release year: ')
            genre = input('Enter the genre: ')
            book = Book(generate_book_id(), title, author, release_year, genre)
            library.add_new_book(book)
            librarian_interface()
        except (
            EmptyTitleError,
            NoAuthorError,
            NoReleaseYearError,
            NoGenreError
        ) as e:
            print(e)
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                librarian_interface()


def add_user(is_librarian=False):
    while True:
        try:
            name = input('Enter the name: ')
            password = getpass('Enter the password: ')
            if is_librarian:
                lib = Librarian(generate_librarian_id(), name, password)
                library.add_new_librarian(lib)
            else:
                user = User(generate_user_id(), name, password)
                library.add_new_user(user)
            librarian_interface()
        except (EmptyNameError, EmptyPasswordError, ShortPasswordError) as e:
            print(e)
            answer = input('Do you want to try again? [y/n] ')
            if answer.lower() != 'y':
                librarian_interface()


def add_book_copy():
    librarian_id_operation(
        library.add_copy_of_book,
        NoBookIDError,
        library_books_librarian_interface,
        'book',
        generate_book_id()
    )


def remove_book():
    librarian_id_operation(
        library.remove_book,
        (BorrowedBookError, NoBookIDError),
        library_books_librarian_interface,
        'book'
    )


def remove_user():
    librarian_id_operation(
        library.remove_user,
        (UserWithBooksError, NoBookIDError),
        library_books_librarian_interface,
        'user'
    )


def remove_librarian():
    librarian_id_operation(
        library.remove_librarian,
        (NoLibrarianIDError, NoBookIDError, RemoveYourselfError),
        library_books_librarian_interface,
        'librarian',
        new_id=None,
        librarian_id=librarian.id
    )


def search_book_librarian_interface():
    filters_list()
    while True:
        for _ in range(3):
            try:
                choice = int(input('Enter your choice: '))
                if choice == 1:
                    search_keyword(search_book_librarian_interface)
                    library_books_librarian_interface()
                elif choice == 2:
                    try:
                        print('\n'.join(library.available_genres()))
                        search_genre(search_book_librarian_interface)
                        library_books_librarian_interface()
                    except GenresNotFoundError as e:
                        print(e)
                        answer = input('Do you want to try again? [y/n] ')
                        if answer.lower() != 'y':
                            librarian_interface()
                        else:
                            search_book_librarian_interface()
                elif choice == 3:
                    try:
                        print('\n'.join(library.available_authors()))
                        search_author(search_book_librarian_interface)
                        library_books_librarian_interface()
                    except AuthorsNotFoundError as e:
                        print(e)
                        answer = input('Do you want to try again? [y/n] ')
                        if answer.lower() != 'y':
                            librarian_interface()
                        else:
                            search_book_librarian_interface()
                elif choice == 4:
                    try:
                        print('\n'.join(library.available_years()))
                        search_year(search_book_librarian_interface)
                        library_books_librarian_interface()
                    except YearsNotFoundError as e:
                        print(e)
                        answer = input('Do you want to try again? [y/n] ')
                        if answer.lower() != 'y':
                            librarian_interface()
                        else:
                            search_book_librarian_interface()
                elif choice == 5:
                    librarian_interface()
                else:
                    raise ValueError
            except ValueError:
                print('Invalid input, try again.')
        else:
            message = ('You have exceeded the maximum number ' +
                       'of attempts. Please try again later.')
            print_with_box(message, len(message) + 2)
            quit()


def library_users_librarian_interface():
    librarians_users_options()
    while True:
        for _ in range(3):
            try:
                choice = int(input('Enter your choice: '))
                if choice == 1:
                    add_user()
                elif choice == 2:
                    add_user(is_librarian=True)
                elif choice == 3:
                    remove_user()
                elif choice == 4:
                    remove_librarian()
                elif choice == 5:
                    librarian_interface()
                else:
                    raise ValueError
            except ValueError:
                print('Invalid input, try again.')
        else:
            message = ('You have exceeded the maximum number ' +
                       'of attempts. Please try again later.')
            print_with_box(message, len(message) + 2)
            quit()

if __name__ == "__main__":
    main()
