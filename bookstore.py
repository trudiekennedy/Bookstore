# Import SQL.
import sqlite3

# Global variables.
books = [(3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
         (3003, "The Lion, the Witch and the Wardrobe", "C.S Lewis", 25),
         (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
         (3005, "Alice in Wonderland", "Lewis Carroll", 12)]

return_to_menu = False  # Flag to aid breaking out of loops & return to main menu.

# Error messages.
id_error = "Sorry, the ID provided doesn't match any books."
menu_error = "Selection not recognised. Please enter a number between 0-4."
not_an_option_error = "Entered value not recognised. Please try again."
number_error = "Entry must be a number. Please try again."


# === FUNCTIONS ===
# Returns options menu.
def bookstore_menu():
    """
    Details the menu options available to the user.
    :return: string with options
    """
    return (f'\n=== MENU ===\n'
            f'1 - Enter Book\n'
            f'2 - Update Book\n'
            f'3 - Delete Book\n'
            f'4 - Search Books \n'
            f'0 - Exit\n')


# Search menu
def search_menu():
    """
    Details the search options available to the user.
    :return: string: search options.
    """
    return (f'\n=== SEARCH OPTIONS ===\n'
            f'1 - Search by ID\n'
            f'2 - Search by Title\n'
            f'3 - Search by Author\n'
            f'4 - Search by Quantity\n'
            f'0 - Return to Main Menu\n')


def connect_to_db():
    """
    Connects to "ebookstore_db" (or creates it if it doesn't exist).
    Creates a table called books (if it doesn't already exist) with fields for primary key, title, author and quantity.
    :return: ebookstore database (or error if exception occurs).
    """
    try:
        database = sqlite3.connect('ebookstore_db')
        func_cursor = database.cursor()
        func_cursor.execute(
            '''CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)''')
        database.commit()
        return database
    except sqlite3.Error as e:
        raise e


def enter_book(database, new_title, new_author, new_quantity):
    """
    Adds a new book to the books table in ebookstore database using given args.
    :param database: relevant database
    :param new_title: title of the new book (string)
    :param new_author: name of the author (string)
    :param new_quantity: quantity of books (integer)
    :return: string: success message that new book has been committed.
    """
    func_cursor = database.cursor()
    func_cursor.execute(""" INSERT INTO books(Title, Author, Qty) VALUES(?, ?, ?)""",
                        (new_title, new_author, new_quantity))
    database.commit()
    return f"Success! Book has been added to the inventory."


def update_book(database, input_key, edit_title, edit_author, edit_quantity):
    """
    Edits a book in the book table of ebookstore database based on the primary key
    :param database: relevant database
    :param input_key: primary key of the entry that needs to be updated (integer)
    :param edit_title: amended title (string)
    :param edit_author: amended author (string)
    :param edit_quantity: amended quantity (integer)
    :return: string: success message once book has been updated.
    """
    func_cursor = database.cursor()
    func_cursor.execute("""UPDATE books SET Title = ?, Author = ?, Qty = ? WHERE id = ?""",
                        (edit_title, edit_author, edit_quantity, input_key))
    database.commit()
    return "Book details have been updated!"


def search_by_title(database, search_title):
    """
    Function that searches for a book by title and returns all books with that title.
    As user may not know full title have used LIKE operator in search: https://www.w3schools.com/SQL/sql_like.asp
    :param database: relevant database
    :param search_title: title or partial title of book being searched for (string)
    :return: string: details of books that match the search entry or "no results found".
    """
    func_cursor = database.cursor()
    func_cursor.execute(""" SELECT * FROM books WHERE Title LIKE ?""", ('%' + search_title + '%',))
    returned_books = func_cursor.fetchall()

    if returned_books:
        for book in returned_books:
            print("{0}: '{1}' by {2} ({3} copies available)".format(book[0], book[1], book[2], book[3]))
    else:
        print("No results found.")


def search_by_quantity(database, operator, qty_provided):
    """
    Finds books that either have a higher, lower or equal quantity of the number input.
    :param database: relevant database.
    :param operator: comparative operator (string).
    :param qty_provided: number quantity (integer).
    :return: string: books from database that match search criteria or "no results found".
    """
    func_cursor = database.cursor()
    if operator == '>':
        func_cursor.execute(""" SELECT * FROM books WHERE Qty > ?""", (qty_provided,))
    elif operator == '<':
        func_cursor.execute(""" SELECT * FROM books WHERE Qty < ?""", (qty_provided,))
    elif operator == '=':
        func_cursor.execute(""" SELECT * FROM books WHERE Qty = ?""", (qty_provided,))

    returned_books = func_cursor.fetchall()

    if returned_books:
        for book in returned_books:
            print("{0}: '{1}' by {2} ({3} copies available)".format(book[0], book[1], book[2], book[3]))
    else:
        print("No results found.")


def search_by_author(database, search_author):
    """
    Function that searches for a book by author based and returns all books by that author.
    User may not know full author details have used LIKE operator in search: https://www.w3schools.com/SQL/sql_like.asp
    :param database: relevant database.
    :param search_author: author or partial name of author (string).
    :return: books that match the search terms (string) or "no results found".
    """
    func_cursor = database.cursor()
    func_cursor.execute(""" SELECT * FROM books WHERE Author LIKE ?""", ('%' + search_author + '%',))
    returned_books = func_cursor.fetchall()

    if returned_books:
        for book in returned_books:
            print("{0}: '{1}' by {2} ({3} copies available)".format(book[0], book[1], book[2], book[3]))
    else:
        print("No results found.")


# Function to search for a book by its primary key.
def search_by_id(database, key):
    """
    Searches for a book in the database by its primary key.
    :param database: relevant database.
    :param key: integer representing the key of the book.
    :return: string: details of the book or an int: 0.
    """
    func_cursor = database.cursor()
    func_cursor.execute(''' SELECT Title, Author, Qty FROM books WHERE id = ?''', (key,))
    returned_book = func_cursor.fetchone()

    # If book is found returns formatted entry (without key). Else returns 0.
    if returned_book:
        return "'{0}' by {1} ({2} copies available)".format(returned_book[0], returned_book[1], returned_book[2])
    else:
        return 0


def delete_book(database, key):
    """
    Deletes a book that matches the primary key passed as an argument into the function.
    :param database: relevant database
    :param key: primary key (integer)
    :return: Message to say whether deletion has been successful or if an error has occurred.
    """
    try:
        func_cursor = database.cursor()
        func_cursor.execute(''' DELETE FROM books WHERE id = ?''', (key,))
        database.commit()
        return f"Book has been deleted successfully"
    except sqlite3.Error:
        database.rollback()
        return f"There has been an error deleting the book from the database."


# === CODE ===
# Connect to database and create a cursor.
db = connect_to_db()
cursor = db.cursor()
# This will push existing books to database. IGNORE INTO will ignore if books already exist in database.
cursor.executemany(''' INSERT OR IGNORE INTO books(id, Title, Author, Qty) VALUES(?, ?, ?, ?) ''', books)
db.commit()

# Display menu to user and ask user to select an option. Present error if option isn't recognised.
# Run relevant function depending on chosen option.
while True:
    print(bookstore_menu())

    try:
        user_selection = int(input("Select action (0-4): "))
    except ValueError:
        print(menu_error)
        continue

    # Exit application.
    if user_selection == 0:
        print("Goodbye!")
        db.close()
        exit()

    # Enter a book.
    if user_selection == 1:
        title = input("Enter book title: ")
        author = input("Enter author: ")

        # Handle value error if quantity is not an integer.
        try:
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print(number_error)
            continue

        print(enter_book(db, title, author, quantity))

    # Update a book.
    elif user_selection == 2:
        while True:
            try:
                p_key = int(input("Enter id of book to update: "))
            except ValueError:  # Handles user input which isn't a number.
                print(number_error)
                continue

            # Runs function to search for book via input provided for 'p_key'.
            # If result is 0 (not found), user will be prompted to enter again. If book found, user asked to confirm.
            result = search_by_id(db, p_key)
            print(f"=== Search Result ===")
            if result == 0:
                print(id_error)
            else:
                print(result)
                confirm = input("Is this the book you want to update? (Y/N): ").upper()

                # If user confirms, title, author and qty will be asked for an updated against key.
                while confirm == "Y":
                    if confirm == "Y":
                        title = input("Enter book title: ")
                        author = input("Enter author: ")
                        try:
                            quantity = int(input("Enter quantity: "))
                        except ValueError:
                            print(number_error)
                            continue

                        print(update_book(db, p_key, title, author, quantity))
                        return_to_menu = True
                        break

                    # If user selects "N", they will be asked to re-input book id.
                    elif confirm == "N":
                        print("This book won't be updated.\n")
                        return_to_menu = False
                        break

                    # Handles where user doesn't input "Y" or "N". User will be asked re-input id.
                    else:
                        print(f"{not_an_option_error}\n")
                        break
                # If return_to_menu is True, loop will break to main menu.
                if return_to_menu:
                    break

    # Delete a book.
    elif user_selection == 3:
        delete_key = 0

        while True:
            try:
                delete_key = int(input("Enter the key of the book you want to delete: "))
                break
            except ValueError:      # Handles error if input not a number.
                print(number_error)
                continue

        # Searches for book by ID provided.
        del_result = search_by_id(db, delete_key)

        # If key doesn't match a book (result = 0) then user is asked for key again.
        while del_result == 0:
            print(id_error)
            delete_key = input("Enter the key of the book you want to delete: ")
            del_result = search_by_id(db, delete_key)

        # If key matches a book, the details of the book are replayed to user.
        print(f"\nYou have selected:\n"
              f"{del_result}")

        # Seeks confirmation that user wants to delete the selected book.
        while True:
            confirm_del = input(f"\nAre you sure you want to delete this book? (Y/N): ").upper()

            if confirm_del == "Y":
                print(delete_book(db, delete_key))
                break
            elif confirm_del == "N":
                print("Deletion cancelled.")
                break
            else:       # Handles input that isn't Y or N.
                print(not_an_option_error)
                continue

    # Search option; displays 4 search functions for user to choose from.
    elif user_selection == 4:
        while True:
            print(search_menu())
            try:
                search_selection = int(input("Select action (0-4): "))
            except ValueError:
                print(menu_error)
                continue

            # Exit search.
            if search_selection == 0:
                break

            # Search by primary key.
            elif search_selection == 1:
                try:
                    p_key = int(input("Enter id of book: "))
                except ValueError:  # Handles user input which isn't a number.
                    print(number_error)
                    continue

                result = search_by_id(db, p_key)

                print("=== Search Result ===")
                if result == 0:
                    print(id_error)
                    print("\n")
                else:
                    print(result)
                    print("\n")

            # Title search.
            elif search_selection == 2:
                user_title = input("Enter the title you want to search: ")
                print("=== Search Results ===")
                search_by_title(db, user_title)

            # Author Search.
            elif search_selection == 3:
                user_author = input("Enter name of the author you want to search: ")
                print("=== Search Results ===")
                search_by_author(db, user_author)

            # Quantity search
            elif search_selection == 4:
                quantity = 0
                while True:
                    try:
                        quantity = int(input("Quantity to search: "))
                        break
                    except ValueError:
                        print(number_error)
                        continue

                while True:
                    print(f"\n=== SEARCH OPERATOR OPTIONS ===\n"
                          f"> - searches for books with more than {quantity} in stock\n"
                          f"< - searches for books with less than {quantity} in stock\n"
                          f"= - searches for books with exactly {quantity} in stock")
                    operator_selection = input("Enter operator option: ")

                    if operator_selection not in ['<', '>', '=']:
                        print(f"\n{not_an_option_error}\n")
                        continue
                    else:
                        print(f"\n=== SEARCH RESULTS===")
                        search_by_quantity(db, operator_selection, quantity)
                        print("")
                        break

            else:
                print(not_an_option_error)
                continue
    else:
        print(not_an_option_error)
        continue
