from class_book import Book
from class_library import Library
from class_user import User, Librarian
from getpass import getpass
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator as max
from prettytable import PrettyTable
from generate_id import (
    generate_book_id,
    generate_user_id,
    generate_librarian_id
)
from print_methods import (
    print_with_box,
    print_with_box_up,
    red,
    green
)
from options_lists import (
    start_options,
    user_options,
    filters_list,
    library_books_options,
    users_books_options,
    librarian_options,
    librarians_books_options,
    librarians_users_options,
    stats_options,
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
current_user = None
current_librarian = None


def main():
    print_with_box_up(' '*9 + 'Library' + ' '*9, 27)
    library_start()


def try_again_later():
    message = ('You have exceeded the maximum number ' +
               'of attempts. Please try again later.')
    print_with_box(message, len(message) + 2)
    quit()


def error_message(message, interface):
    print(red('! ') + str(message))
    answer = input('Do you want to try again? [' +
                   green('y') + '/' + red('n') + '] ')
    if answer.lower() != 'y':
        interface()


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
                print(red('! ') + 'Invalid input, try again.')
        else:
            try_again_later()


def login():
    global current_user, current_librarian
    while True:
        try:
            id = int(input('Enter your ID: '))
            password = getpass('Enter your password: ')
            check = library.login_role_check(id, password)
            if check:
                if str(check["id"]).startswith('1'):
                    current_librarian = Librarian(**check)
                    message = f'Welcome, {current_librarian.name}!'
                    print_with_box(message, len(message) + 2)
                    librarian_interface()
                else:
                    current_user = User(**check)
                    message = f'Welcome to our library, {current_user.name}!'
                    print_with_box(message, len(message) + 2)
                    user_interface()
            else:
                raise WrongIDError
        except (WrongPasswordError, WrongIDError) as e:
            error_message(e, library_start)
        except ValueError:
            error_message('Incorrect ID.', library_start)


def create_account():
    global current_user
    while True:
        try:
            name = input('Enter your name: ')
            password = getpass('Enter your password: ')
            current_user = User(generate_user_id(), name, password)
            library.add_new_user(current_user)
            id = current_user.id
            name = current_user.name
            message = f'Welcome to our library, {name}! Your ID is {id}'
            print_with_box(message, len(message) + 2)
            user_interface()
        except (EmptyNameError, EmptyPasswordError, ShortPasswordError) as e:
            error_message(e, library_start)


def user_interface():
    while True:
        user_options()
        for _ in range(3):
            try:
                choice = int(input('Enter your choice: '))
                if choice == 1:
                    result = PrettyTable()
                    result.field_names = ["ID",
                                          "Title",
                                          "Author",
                                          "Release Year",
                                          "Genre",
                                          "Loan history",
                                          "Current owner",
                                          "Extensions",
                                          "Reservations",
                                          "Return date"]
                    rows = library.available_books_info()
                    result.add_rows(rows)
                    print(result)
                    library_books_user_interface()
                elif choice == 2:
                    search_book_user_interface()
                elif choice == 3:
                    if not current_user.borrowed_books:
                        print('Borrowed books:\n' +
                              'You do not have any books at the moment.')
                    else:
                        borrowed = PrettyTable()
                        borrowed.field_names = ["ID",
                                                "Title",
                                                "Author",
                                                "Reservations",
                                                "Return date"]
                        rows = current_user.get_borrowed_books()
                        borrowed.add_rows(rows)
                        print('Borrowed books:\n' + borrowed.get_string())
                    if not current_user.borrowing_history:
                        print('Borrowing history:\n' +
                              'You have not borrowed any books yet.')
                    else:
                        history = PrettyTable()
                        history.field_names = ["ID",
                                               "Title",
                                               "Author"]
                        rows = current_user.get_history()
                        history.add_rows(rows)
                        print('Borrowing history:\n' + history.get_string())
                    if not current_user.reservations:
                        inf = 'You do not have any reservations at the moment.'
                        print('Reservations:\n' + inf)
                    else:
                        reservations = PrettyTable()
                        reservations.field_names = ["ID",
                                                    "Title",
                                                    "Author",
                                                    "Position in queue",
                                                    "Return date"]
                        rows = current_user.get_reservations()
                        reservations.add_rows(rows)
                        print('Reservations:\n' + reservations.get_string())
                    users_books_interface()
                elif choice == 4:
                    get_stats(user_interface)
                elif choice == 5:
                    library_start()
                else:
                    raise ValueError
            except ValueError:
                print(red('! ') + 'Invalid input, try again.')
        else:
            try_again_later()
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
                        error_message(e, user_interface)
                        search_book_user_interface()
                elif choice == 3:
                    try:
                        print('\n'.join(library.available_authors()))
                        search_author(search_book_user_interface)
                        library_books_user_interface()
                    except AuthorsNotFoundError as e:
                        error_message(e, user_interface)
                        search_book_user_interface()
                elif choice == 4:
                    try:
                        print('\n'.join(library.available_years()))
                        search_year(search_book_user_interface)
                        library_books_user_interface()
                    except YearsNotFoundError as e:
                        error_message(e, user_interface)
                        search_book_user_interface()
                elif choice == 5:
                    user_interface()
                else:
                    raise ValueError
            except ValueError:
                print(red('! ') + 'Invalid input, try again.')
        else:
            try_again_later()


def search_by(option, errors, search_interface):
    while True:
        try:
            result = option()
            print(result)
            break
        except errors as e:
            error_message(e, search_interface)
        except ValueError:
            error_message('Incorrect input.', search_interface)


def search_keyword(search_interface):
    def keyword():
        global library
        keyword = input('Enter the keyword: ')
        result = PrettyTable()
        result.field_names = ["ID",
                              "Title",
                              "Author",
                              "Release Year",
                              "Genre",
                              "Loan history",
                              "Current owner",
                              "Extensions",
                              "Reservations",
                              "Return date"]
        rows = library.search_book_by_keyword(keyword)
        result.add_rows(rows)
        return result
    search_by(
        keyword,
        (NoKeywordError, KeywordNotFoundError),
        search_interface
    )


def search_genre(search_interface):
    def genre():
        global library
        genre = input('Enter the genre: ')
        result = PrettyTable()
        result.field_names = ["ID",
                              "Title",
                              "Author",
                              "Release Year",
                              "Genre",
                              "Loan history",
                              "Current owner",
                              "Extensions",
                              "Reservations",
                              "Return date"]
        rows = library.search_book_by_genre(genre)
        result.add_rows(rows)
        return result
    search_by(
        genre,
        UnavailableGenreError,
        search_interface
    )


def search_author(search_interface):
    def author():
        global library
        author = input('Enter the author: ')
        result = PrettyTable()
        result.field_names = ["ID",
                              "Title",
                              "Author",
                              "Release Year",
                              "Genre",
                              "Loan history",
                              "Current owner",
                              "Extensions",
                              "Reservations",
                              "Return date"]
        rows = library.search_book_by_author(author)
        result.add_rows(rows)
        return result
    search_by(
        author,
        UnavailableAuthorError,
        search_interface
    )


def search_year(search_interface):
    def year():
        global library
        year = input('Enter the year: ')
        result = PrettyTable()
        result.field_names = ["ID",
                              "Title",
                              "Author",
                              "Release Year",
                              "Genre",
                              "Loan history",
                              "Current owner",
                              "Extensions",
                              "Reservations",
                              "Return date"]
        rows = library.search_book_by_year(year)
        result.add_rows(rows)
        return result
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
                print(red('! ') + 'Invalid input, try again.')
        else:
            try_again_later()


def user_operation(operation, errors, interface):
    while True:
        try:
            book_id = int(input('Enter book ID: '))
            operation(book_id)
            library.update_data()
            interface()
        except errors as e:
            error_message(e, user_interface)
            interface()

        except ValueError:
            error_message('Incorrect ID.', user_interface)
            interface()


def borrow_book():
    user_operation(
        current_user.borrow_book,
        (UsersBookError, BorrowedBookError, NoBookIDError),
        library_books_user_interface
    )


def reserve_book():
    user_operation(
        current_user.reserve_book,
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
                print(red('! ') + 'Invalid input, try again.')
        else:
            try_again_later()


def return_book():
    user_operation(
        current_user.return_book,
        (NotUsersBookError, NoBookIDError),
        users_books_interface
    )


def use_extension():
    user_operation(
        current_user.use_extension,
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
        current_user.cancel_reservation,
        (NotUsersBookError, NoBookIDError),
        users_books_interface
    )


def get_stats(interface):
    stats_options()
    while True:
        for _ in range(3):
            try:
                choice = int(input('Enter your choice: '))
                if choice == 1:
                    books = list(library.get_books_stats().keys())
                    stats = list(library.get_books_stats().values())
                    plt.barh(books, stats)
                    plt.xlabel("Titles")
                    plt.ylabel("Total loans")
                    plt.title("Books stats")
                    plt.gca().xaxis.set_major_locator(max(integer=True))
                    plt.tight_layout()
                    plt.show()
                    get_stats(interface)
                elif choice == 2:
                    users = list(library.get_users_stats().keys())
                    stats = list(library.get_users_stats().values())
                    plt.barh(users, stats)
                    plt.ylabel("Names")
                    plt.xlabel("Borrowed books")
                    plt.title("Users stats")
                    plt.gca().xaxis.set_major_locator(max(integer=True))
                    plt.tight_layout()
                    plt.show()
                    get_stats(interface)
                elif choice == 3:
                    interface()
                else:
                    raise ValueError
            except ValueError:
                print(red('! ') + 'Invalid input, try again.')
        else:
            try_again_later()


def librarian_interface():
    while True:
        librarian_options()
        for _ in range(3):
            try:
                choice = int(input('Enter your choice: '))
                if choice == 1:
                    result = PrettyTable()
                    result.field_names = ["ID",
                                          "Title",
                                          "Author",
                                          "Release Year",
                                          "Genre",
                                          "Loan history",
                                          "Current owner",
                                          "Extensions",
                                          "Reservations",
                                          "Return date"]
                    rows = library.available_books_info()
                    result.add_rows(rows)
                    print(result)
                    library_books_librarian_interface()
                elif choice == 2:
                    search_book_librarian_interface()
                elif choice == 3:
                    users, librarians = library.users_librarians()
                    if not users:
                        print('Users:\n' +
                              'Users not found.')
                    else:
                        users_table = PrettyTable()
                        users_table.field_names = ["ID",
                                                   "Name",
                                                   "Password",
                                                   "Borrowed books",
                                                   "Reservations",
                                                   "Borrowing history"]
                        users_table.add_rows(users)
                        print('Users:\n' + users_table.get_string())
                    if not librarians:
                        print('Librarians:\n' +
                              'Librarians not found.')
                    else:
                        librarians_table = PrettyTable()
                        librarians_table.field_names = ["ID",
                                                        "Name",
                                                        "Password"]
                        librarians_table.add_rows(librarians)
                        print('Librarians:\n' + librarians_table.get_string())
                    library_users_librarian_interface()
                elif choice == 4:
                    search_users_librarian()
                    library_users_librarian_interface()
                elif choice == 5:
                    get_stats(librarian_interface)
                elif choice == 6:
                    library_start()
                else:
                    raise ValueError
            except ValueError:
                print(red('! ') + 'Invalid input, try again.')
        else:
            try_again_later()
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
                print(red('! ') + 'Invalid input, try again.')
        else:
            try_again_later()


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
            interface()
        except errors as e:
            error_message(e, librarian_interface)
            interface()

        except ValueError:
            error_message('Incorrect ID.', librarian_interface)
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
            library_books_librarian_interface()
        except (
            EmptyTitleError,
            NoAuthorError,
            NoReleaseYearError,
            NoGenreError
        ) as e:
            error_message(e, librarian_interface)


def add_user(is_librarian=False):
    while True:
        try:
            name = input('Enter the name: ')
            password = getpass('Enter the password: ')
            if is_librarian:
                librarian = Librarian(generate_librarian_id(), name, password)
                library.add_new_librarian(librarian)
            else:
                user = User(generate_user_id(), name, password)
                library.add_new_user(user)
            library_users_librarian_interface()
        except (EmptyNameError, EmptyPasswordError, ShortPasswordError) as e:
            error_message(e, librarian_interface)


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
        library_users_librarian_interface,
        'user'
    )


def remove_librarian():
    librarian_id_operation(
        library.remove_librarian,
        (NoLibrarianIDError, NoBookIDError, RemoveYourselfError),
        library_users_librarian_interface,
        'librarian',
        new_id=None,
        librarian_id=current_librarian.id
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
                        error_message(e, librarian_interface)
                        search_book_librarian_interface()
                elif choice == 3:
                    try:
                        print('\n'.join(library.available_authors()))
                        search_author(search_book_librarian_interface)
                        library_books_librarian_interface()
                    except AuthorsNotFoundError as e:
                        error_message(e, librarian_interface)
                        search_book_librarian_interface()
                elif choice == 4:
                    try:
                        print('\n'.join(library.available_years()))
                        search_year(search_book_librarian_interface)
                        library_books_librarian_interface()
                    except YearsNotFoundError as e:
                        error_message(e, librarian_interface)
                        search_book_librarian_interface()
                elif choice == 5:
                    librarian_interface()
                else:
                    raise ValueError
            except ValueError:
                print('Invalid input, try again.')
        else:
            try_again_later()


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
            try_again_later()


def search_users_librarian():
    global library
    while True:
        try:
            keyword = input('Enter the keyword (or ID): ')
            users, librarians = library.search_user(keyword)
            if not users:
                print('Users:\n' +
                      'No users found matching the provided keyword.')
            else:
                users_table = PrettyTable()
                users_table.field_names = ["ID",
                                           "Name",
                                           "Password",
                                           "Borrowed books",
                                           "Reservations",
                                           "Borrowing history"]
                users_table.add_rows(users)
                print('Users:\n' + users_table.get_string())
            if not librarians:
                print('Librarians:\n' +
                      'No librarians found matching the provided keyword.')
            else:
                librarians_table = PrettyTable()
                librarians_table.field_names = ["ID",
                                                "Name",
                                                "Password"]
                librarians_table.add_rows(librarians)
                print('Librarians:\n' + librarians_table.get_string())
            break
        except (NoKeywordError, KeywordNotFoundError) as e:
            error_message(e, librarian_interface)
        except ValueError:
            error_message('Incorrect input.', librarian_interface)


if __name__ == "__main__":
    main()


# dodac kolorowy tekst komunikatow z nowa metoda
# dodac komunikaty powitalne, dodania, usuniecia, wypozyczenia, itp.
