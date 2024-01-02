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
    NoUserIDError,
    NotReservedError,
    DoubleReservationBookError
)

library = Library()
current_user = None
current_librarian = None


def main():
    """
    Entry point of the library management system.
    """
    print_with_box_up(' '*9 + 'Library' + ' '*9, 27)
    library_start()


def try_again_later():
    """
    Prints a message for exceeding the maximum number of attempts.
    """
    message = ('You have exceeded the maximum number ' +
               'of attempts. Please try again later.')
    print_with_box(message, len(message) + 2)
    quit()


def error_message(message, interface):
    """
    Prints an error message and prompts the user to try again.
    """
    print(red(f'! {message}'))
    answer = input('Do you want to try again? [' +
                   green('y') + '/' + red('n') + '] ')
    if answer.lower() != 'y':
        interface()


def books_table():
    """
    Prints a table with information about available books.
    """
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


def users_librarians_table(users, librarians):
    """
    Prints tables with information about users and librarians.
    """
    if not users:
        print('Users: ' + red('None'))
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
        print('Librarians: ' + red('None'))
    else:
        librarians_table = PrettyTable()
        librarians_table.field_names = ["ID",
                                        "Name",
                                        "Password"]
        librarians_table.add_rows(librarians)
        print('Librarians:\n' + librarians_table.get_string())


def users_books_table():
    """
    Prints tables with information about a user's borrowed books,
    borrowing history, and reservations.
    """
    if not current_user.borrowed_books:
        print('Borrowed books: ' + red('None'))
    else:
        borrowed = PrettyTable()
        borrowed.field_names = ["ID",
                                "Title",
                                "Author",
                                "Extensions",
                                "Reservations",
                                "Return date"]
        rows = current_user.get_borrowed_books()
        borrowed.add_rows(rows)
        print('Borrowed books:\n' + borrowed.get_string())
    if not current_user.borrowing_history:
        print('Borrowing history: ' + red('None'))
    else:
        history = PrettyTable()
        history.field_names = ["ID",
                               "Title",
                               "Author"]
        rows = current_user.get_history()
        history.add_rows(rows)
        print('Borrowing history:\n' + history.get_string())
    if not current_user.reservations:
        print('Reservations: ' + red('None'))
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


def library_start():
    """
    Displays start options and handles user input.
    """
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
                print(red('! Invalid input, try again.'))
        else:
            try_again_later()


def login():
    """
    Handles user login, validates credentials, and directs
    to user or librarian interface.
    """
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
                    print(library.return_date_check(current_user.id))
                    user_interface()
            else:
                raise WrongIDError
        except (WrongPasswordError, WrongIDError) as e:
            error_message(e, library_start)
        except ValueError:
            error_message('Incorrect ID.', library_start)


def create_account():
    """
    Handles the creation of a new user account.
    """
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
    """
    Displays user interface options and handles user input.
    """
    while True:
        user_options()
        for _ in range(3):
            try:
                choice = int(input('Enter your choice: '))
                if choice == 1:
                    books_table()
                    library_books_user_interface()
                elif choice == 2:
                    search_book_user_interface()
                elif choice == 3:
                    users_books_table()
                    users_books_interface()
                elif choice == 4:
                    get_stats(user_interface)
                elif choice == 5:
                    library_start()
                else:
                    raise ValueError
            except ValueError:
                print(red('! Invalid input, try again.'))
        else:
            try_again_later()
        break


def search_book_user_interface():
    """
    Displays search options for users and handles user input.
    """
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
                print(red('! Invalid input, try again.'))
        else:
            try_again_later()


def search_by(option, errors, search_interface):
    """
    Helper function to perform a search operation.
    """
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
    """
    Searches for books based on a keyword provided by the user.
    """
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
    """
    Searches for books based on a genre provided by the user.
    """
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
    """
    Searches for books based on an author provided by the user.
    """
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
    """
    Searches for books based on a release year provided by the user.
    """
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
    """
    Displays book options for users and handles user input.
    """
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
                print(red('! Invalid input, try again.'))
        else:
            try_again_later()


def user_operation(operation, errors, interface, table):
    """
    Generic function to perform user operations like borrowing, returning, etc.
    """
    while True:
        try:
            book_id = int(input('Enter book ID: '))
            message = operation(book_id)
            library.update_data()
            table()
            print(green(str(message)))
            interface()
        except errors as e:
            error_message(e, user_interface)
            interface()

        except ValueError:
            error_message('Incorrect ID.', user_interface)
            interface()


def borrow_book():
    """
    Handles the borrowing of a book by a user.
    """
    user_operation(
        current_user.borrow_book,
        (UsersBookError, BorrowedBookError, NoBookIDError),
        library_books_user_interface, books_table
    )


def reserve_book():
    """
    Handles the reservation of a book by a user.
    """
    user_operation(
        current_user.reserve_book,
        (UsersBookError,
         NoBookOwnerError,
         NoBookIDError,
         DoubleReservationBookError),
        library_books_user_interface, books_table
    )


def users_books_interface():
    """
    Displays options for users regarding their books,
    reservations, etc., and handles user input.
    """
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
                print(red('! Invalid input, try again.'))
        else:
            try_again_later()


def return_book():
    """
    Handles the return of a book by a user.
    """
    user_operation(
        current_user.return_book,
        (NotUsersBookError, NoBookIDError),
        users_books_interface, users_books_table
    )


def use_extension():
    """
    Handles the extension of a book loan by a user.
    """
    user_operation(
        current_user.use_extension,
        (
            NotUsersBookError,
            ReservedBookError,
            NotEnoughExtensionsError,
            NoBookIDError
        ),
        users_books_interface,
        users_books_table
    )


def cancel_reservation():
    """
    Handles the cancellation of a book reservation by a user.
    """
    user_operation(
        current_user.cancel_reservation,
        (NotUsersBookError, NoBookIDError, NotReservedError),
        users_books_interface, users_books_table
    )


def get_stats(interface):
    """
    Displays statistics options and handles user
    input to generate and display statistics.
    """
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
                print(red('! Invalid input, try again.'))
        else:
            try_again_later()


def librarian_interface():
    """
    Displays librarian interface options and handles user input.
    """
    while True:
        librarian_options()
        for _ in range(3):
            try:
                choice = int(input('Enter your choice: '))
                if choice == 1:
                    books_table()
                    library_books_librarian_interface()
                elif choice == 2:
                    search_book_librarian_interface()
                elif choice == 3:
                    users, librarians = library.users_librarians()
                    users_librarians_table(users, librarians)
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
                print(red('! Invalid input, try again.'))
        else:
            try_again_later()
        break


def library_books_librarian_interface():
    """
    Displays books options for librarians and handles user input.
    """
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
                print(red('! Invalid input, try again.'))
        else:
            try_again_later()


def librarian_id_operation(
        operation,
        errors,
        interface,
        obj_id,
        table=books_table,
        new_id=None,
        librarian_id=None,
        ):
    """
    Generic function to perform librarian operations
    like adding, removing, etc.
    """
    global librarian
    while True:
        try:
            id = int(input(f'Enter {obj_id} ID: '))
            if new_id:
                message = operation(id, new_id)
            elif librarian_id:
                message = operation(id, librarian_id)
            else:
                message = operation(id)
            library.update_data()
            if table == users_librarians_table:
                users, librarians = library.users_librarians()
                table(users, librarians)
            else:
                table()
            print(green(str(message)))
            interface()
        except errors as e:
            error_message(e, librarian_interface)
            interface()
        except ValueError:
            error_message('Incorrect ID.', librarian_interface)
            interface()


def add_book():
    """
    Handles the addition of a new book by a librarian.
    """
    while True:
        try:
            title = input('Enter the title: ')
            author = input('Enter the author: ')
            release_year = input('Enter the release year: ')
            genre = input('Enter the genre: ')
            book = Book(generate_book_id(), title, author, release_year, genre)
            message = library.add_new_book(book)
            books_table()
            print(green(str(message)))
            library_books_librarian_interface()
        except (
            EmptyTitleError,
            NoAuthorError,
            NoReleaseYearError,
            NoGenreError
        ) as e:
            error_message(e, librarian_interface)


def add_user(is_librarian=False):
    """
    Handles the addition of a new user or librarian by a librarian.
    """
    while True:
        try:
            name = input('Enter the name: ')
            password = getpass('Enter the password: ')
            if is_librarian:
                librarian = Librarian(generate_librarian_id(), name, password)
                message = library.add_new_librarian(librarian)
                users, librarians = library.users_librarians()
                users_librarians_table(users, librarians)
                print(green(str(message)))
            else:
                user = User(generate_user_id(), name, password)
                message = library.add_new_user(user)
                users, librarians = library.users_librarians()
                users_librarians_table(users, librarians)
                print(green(str(message)))
            library_users_librarian_interface()
        except (EmptyNameError, EmptyPasswordError, ShortPasswordError) as e:
            error_message(e, librarian_interface)


def add_book_copy():
    """
    Handles the addition of a new copy of a book by a librarian.
    """
    librarian_id_operation(
        library.add_copy_of_book,
        NoBookIDError,
        library_books_librarian_interface,
        'book',
        new_id=generate_book_id(),
    )


def remove_book():
    """
    Handles the removal of a book by a librarian.
    """
    librarian_id_operation(
        library.remove_book,
        (BorrowedBookError, NoBookIDError),
        library_books_librarian_interface,
        'book',
    )


def remove_user():
    """
    Handles the removal of a user by a librarian.
    """
    librarian_id_operation(
        library.remove_user,
        (UserWithBooksError, NoUserIDError),
        library_users_librarian_interface,
        'user',
        table=users_librarians_table
    )


def remove_librarian():
    """
    Handles the removal of a librarian by a librarian.
    """
    librarian_id_operation(
        library.remove_librarian,
        (NoLibrarianIDError, RemoveYourselfError),
        library_users_librarian_interface,
        'librarian',
        new_id=None,
        librarian_id=current_librarian.id,
        table=users_librarians_table
    )


def search_book_librarian_interface():
    """
    Displays search options for librarians and handles user input.
    """
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
                print(red('! Invalid input, try again.'))
        else:
            try_again_later()


def library_users_librarian_interface():
    """
    Displays options for librarians regarding
    library users and handles user input.
    """
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
                print(red('! Invalid input, try again.'))
        else:
            try_again_later()


def search_users_librarian():
    """
    Searches for users or librarians based on
    a keyword or ID provided by the librarian.
    """
    global library
    while True:
        try:
            keyword = input('Enter the keyword (or ID): ')
            users, librarians = library.search_user(keyword)
            users_librarians_table(users, librarians)
            break
        except (NoKeywordError, KeywordNotFoundError) as e:
            error_message(e, librarian_interface)
        except ValueError:
            error_message('Incorrect input.', librarian_interface)


if __name__ == "__main__":
    main()
