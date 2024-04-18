# ================= Compulsory Task Capstone Project =================

# Creating database table
# Creating database table
import sqlite3
import os
db_exists = os.path.exists('ebookstore.db')
db = sqlite3.connect('ebookstore.db')
cursor = db.cursor()  # Getting cursor object

if not db_exists:
    cursor.execute('''
        CREATE TABLE ebookstore(id INTEGER, title TEXT,
               author TEXT, qty INTEGER)
    ''')
    db.commit()


# =====================================================================================================
# Function to insert books into database
def insert_book(cursor, id, title, author, qty):
    try:
        cursor.execute('''INSERT INTO ebookstore(id, title, author, qty)
                      VALUES(?,?,?,?)''', (id, title, author, qty))
        db.commit()
    except sqlite3.IntegrityError:
        print(f"Book {id} already exists in the database.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Retrieving all the books in the database
def all_books():
    cursor.execute('''SELECT id, title FROM ebookstore''')
    books = cursor.fetchall()
    for book in books:
        id, title, author = book
        print(f"\nID: {id}, Title: '{title}'")


def book_details():
    while True:
        try:
            new_book_id = int(input("Enter the ID of the book:\n"))
            new_book_title = str(input("Enter the title of the book:\n"))
            new_book_author = str(input("Enter the author name:\n"))
            new_book_qty = int(input("Add quantity of books:\n"))
            new_book_details = [new_book_id, new_book_title,
                                new_book_author, new_book_qty]
            return new_book_details
        except ValueError:
            print("Invalid input. Please enter the correct values.")


# updating details of books existing in the database
def update_book(new_book_id, new_book_title, new_book_author, new_book_qty,
                book_to_update_id):
    cursor.execute('''UPDATE ebookstore SET id = ?, title = ?, author = ?,
                   qty = ? WHERE id = ?''',
                   (new_book_id, new_book_title, new_book_author,
                    new_book_qty, book_to_update_id))
    db.commit()


# Deleting a book from the database
def delete_book(book_to_delete_id):
    cursor.execute('''DELETE FROM ebookstore WHERE id = ?''',
                   (book_to_delete_id,))
    db.commit()


# Retrieving a particular book in the database
def search_book(book_id_search):
    cursor.execute('''SELECT id, title, author, qty FROM ebookstore
                    WHERE id = ?''', (book_id_search,))
    book = cursor.fetchone()
    print(book)


# =====================================================================================================
# Initialiing database with a list of books
books = [
        (3001, 'A tale of Two Cities', 'Charles Dickens', 30),
        (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K Rowling', 40),
        (3003, 'The Lion, the witch and the Wardrobe', 'C.S. Lewis', 25),
        (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37),
        (3005, 'Alice in Wonderland', 'Lewis Carroll', 12),
        (3006, 'The mind of South Africa', 'Allister Sparks', 25),
        (3007, 'The end of everything', 'Katie Mack', 44)
        ]
for book in books:
    insert_book(cursor, *book)

# Menu options of ebook program
while True:
    # Providing and promting user to select a database query(option)
    print("\nNightville e-Library")
    option = int(input('''Select a menu option
                1. Enter a book - adding a new book to database
                2. Update book - update book information
                3. Delete book - deleting book from database
                4. Search book - retriving books from the database
                5. Exit\n'''))
    
    # User option to add a new book to database
    if option == 1:
        insert_book(cursor, *book_details())
        print("\nBook has been successfully added to the database")

    # User option to update book information
    elif option == 2:
        all_books()
        book_to_update_id = int(input("Which book would you like to update:\n"))
        update_book(*book_details(), book_to_update_id)
        print("Database has been updated with the book.")

    # User option to delete a book
    elif option == 3:
        all_books()
        book_to_delete_id = int(input("Which book would you like to delete:\n"))
        delete_book(book_to_delete_id)
        print("book has been successfully deleted from database.")

    # User option to search a book
    elif option == 4:
        book_id_search = int(input("Which book would you like to view?:\n"))
        search_book(book_id_search)

    # User exist the database
    else:
        print('''You have selected to exit the database. Goodbye!''')
        break

db.commit()
db.close()