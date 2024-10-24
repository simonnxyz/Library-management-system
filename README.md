# **LIBRARY APPLICATION PROJECT**

### Author Details

- Name: Kacper Siemionek
- Student ID: 331430

## **1. Project Goal and Description**

The aim of the project is to design a library application that enables management of the book collection and user/librarian accounts. The application provides an interface for users, allowing them to browse, borrow, and reserve books, check statistics, and for librarians to manage the collection, add new books and copies, and manage user accounts.

### Available Classes:

- *Book*:
  Represents a single copy with a unique identifier. It contains information about the title, author, publication year, genre, history, current holder, reservations, etc.

- *User*:
  Represents a library user with attributes related to personal data, loans, reservations, and a unique identifier. It allows managing loans and reservations.

- *Librarian*:
  Inherits from the user class and also has a name, password, and unique identifier. The librarian has access to internal library methods, such as managing the collection and user accounts.

- *Library*:
  The library class is a crucial component, as it is called every time the application is launched and stores data for all books and users, which it retrieves from JSON files. The main operations enabled by the library include managing available books and users, checking return deadlines, searching for books with filters, providing statistics, etc.

### Operation Description

The library interface begins with the login process. Based on the provided ID, the appropriate interface is assigned according to the detected role:

- The user receives information about any overdue returns and access to options for checking and searching available books, where they can borrow or reserve one of them. Additionally, the user can view their loan history, check book and user statistics, and has the option to log out.

- The librarian initially has similar options, but unlike the user, they have additional methods allowing them to manage the collection and user accounts.

## **2. Installation Instructions and Running the Application**

To ensure the application runs correctly, the required libraries must be installed using the requirements.txt file by executing the following command:

```bash
pip install -r requirements.txt
```

Run the application by executing:

```bash
python3 main.py
```

## **3. Sample Data**

Sample user and book data have been added to the library’s JSON files, allowing observation of the correct functioning of all available features.

### Logging in as a Librarian

To log in as a librarian, use the following credentials:

- **ID:** 1879
- **Password:** admin123

### Using the Library as a Reader

To use the library as a reader, simply create a user account after launching the application.