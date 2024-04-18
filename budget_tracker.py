# ========================= Budget Tracker Application =================
# Application allows a user to add, view and delete transactions.
# Application code is segmented into 3-main parts, viz;
# Part 1: Database set up.
# Part 2: Functions definitions including dictionary.
# Part 3: Main loop of the application.

# ========================= Part 1 =====================================
# Database setup.

# Import libraries.
import sqlite3
import os

# Connect to databse if it already exists.
db_exists = os.path.exists('budget_tracker.db')
db = sqlite3.connect('budget_tracker.db')
cursor = db.cursor()

# Create database tables if database does not already exist.
# Create transactions table.
if not db_exists:
    cursor.execute('''
        CREATE TABLE budget_tracker(Trans_ID INTEGER PRIMARY KEY,
        Trans_Type TEXT, Trans_Category TEXT, Trans_Description TEXT,
        Trans_Amount INTEGER)
    ''')
    db.commit()

# Create tables for budget and financial goals.
if not db_exists:
    cursor.execute('''
        CREATE TABLE budget(Category TEXT, Amount INTEGER)
    ''')
    cursor.execute('''
        CREATE TABLE financial_goals(Category TEXT, Goal INTEGER)
    ''')
    db.commit()


# ========================= Part 2 =====================================
# Functions definition.

# Functions for user interaction.
# Transaction options (Menu).
def transaction_options():
    print("\n" + "="*50)
    print("Transactions Menu:")
    print("-"*50)
    print('''
    1. Add expense
    2. View expenses
    3. View expenses by category
    4. Add income
    5. View income
    6. View income by category
    7. Set budget for a category
    8. View budget for a category
    9. Set financial goal
    10. View progress towards financial goals
    11. Delete a transaction
    12. Delete a category
    13. Quit ''')
    print("="*50 + "\n")


# Function that receives the transaction to be performed by user.
def get_transaction():
    while True:
        try:
            transaction = int(input('''Enter the transaction to be performed \
from 1-13:\n'''))
            if 1 <= transaction <= 13:
                return transaction
            else:
                print('''Error: Transaction out of menu range!''')
        except ValueError:
            print('''That's not a valid input!. Please enter a valid \
transaction from 1 to 13.''')


# Function that alllows user to add a transaction to db.
def add_transaction(transaction_type):
    while True:
        new_tranasction_category = (input('''Enter transaction \
category (medical, salary, loans etc.):\n''')).lower()
        new_transaction_description = (input('''Enter transaction \
description (tooth_filling, feb_salary etc):\n''')).lower()
        new_transaction_amount = input("Enter transaction amount:\n")
        if not new_transaction_amount.isdigit():
            print("Invalid transaction amount. Please enter an integer.")
            continue
        new_transaction_amount = int(new_transaction_amount)
        if transaction_type == "expense":
            new_transaction_amount = (-1)*new_transaction_amount
        cursor.execute('''
            INSERT INTO budget_tracker(Trans_Type, Trans_Category,
            Trans_Description, Trans_Amount) VALUES(?,?,?,?)
        ''', (transaction_type, new_tranasction_category,
              new_transaction_description, new_transaction_amount))
        db.commit()
        print("\nTransaction has been successfully added to the database")
        break


# Function to set budget for a category.
def set_budget():
    category = input("Enter category to set budget:\n").lower()
    while True:
        try:
            amount = int(input("Enter category budget amount:\n"))
            break
        except ValueError:
            print("Invalid input. Please enter a valid budget amount.")
    cursor.execute('''
        INSERT INTO budget(Category, Amount) VALUES(?,?)
    ''', (category, amount))
    db.commit()
    print("\nBudget has been successfully set")


# Function to set financial goal for a category
def set_financial_goal():
    category = input("Enter category to set financial goal:\n").lower()
    while True:
        try:
            goal = int(input("Enter financial goal:\n"))
            if goal <= 0:
                print('''Invalid input. The financial goal must be \
a positive number greater than 0.''')
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid financial goal.")

    cursor.execute('''
        SELECT * FROM financial_goals WHERE Category = ?
    ''', (category,))
    existing_category = cursor.fetchone()

    if existing_category is None:
        cursor.execute('''
            INSERT INTO financial_goals(Category, Goal) VALUES(?,?)
        ''', (category, goal))
    else:
        cursor.execute('''
            UPDATE financial_goals SET Goal = ? WHERE Category = ?
        ''', (goal, category))

    db.commit()
    print("\nFinancial goal has been successfully set.")


# Function for view tranasctions by type.
def transaction_type_view(view_type):
    cursor.execute('''SELECT Trans_ID, Trans_Type, Trans_Category,
   Trans_Description, Trans_Amount FROM budget_tracker
                    WHERE Trans_Type = ?''', (view_type,))
    transaction = cursor.fetchall()
    if transaction:
        print(f'''\n{'ID':<5} {'Type':<10} {'Category':<15} \
{'Description':<30} {'Amount':<10}''')
        print("-"*70)
        for trans_id, trans_type, trans_category, trans_description, \
                trans_amount in transaction:
            print(f"{trans_id:<5} {trans_type:<10} {trans_category:<15} \
{trans_description:<30} {trans_amount:<10}")
    else:
        print(f"There are no {view_type} transactions in the database.")


# Function for view tranasctions by category.
def transaction_category_view(view_category):
    cursor.execute('''SELECT Trans_ID, Trans_Type, Trans_Category,
   Trans_Description, Trans_Amount FROM budget_tracker
                    WHERE Trans_Category = ?''', (view_category,))
    transaction = cursor.fetchall()
    if transaction:
        print(f'''\n{'ID':<5} {'Type':<10} {'Category':<15} \
{'Description':<30} {'Amount':<10}''')
        print("-"*70)
        for trans_id, trans_type, trans_category, trans_description, \
                trans_amount in transaction:
            print(f'''{trans_id: <5} {trans_type:<10} {trans_category:<15} \
{trans_description:<30} {trans_amount:<10}''')
    else:
        print(f"\nThere is no {view_category} category.")


# Function to view budget by category.
def view_budget():
    category = input("Enter budget category to view:\n").lower()
    cursor.execute('''
        SELECT Amount FROM budget WHERE Category = ?
    ''', (category,))
    amount = cursor.fetchone()
    if amount is not None:
        print(f"\nThe budget for {category} is {amount[0]}")
    else:
        print(f"\nNo budget has been set for {category}.")


# Function to view progress towards financial goal by category.
def view_progress():
    category = input("Enter category of financial goal to view:\n").lower()
    cursor.execute('''
        SELECT Goal FROM financial_goals WHERE Category = ?
    ''', (category,))
    goal = cursor.fetchone()
    cursor.execute('''
        SELECT SUM(Trans_Amount) FROM budget_tracker WHERE Trans_Category = ?
    ''', (category,))
    total = cursor.fetchone()
    if goal and total and goal[0] and total[0]:
        progress = round(total[0] / goal[0] * 100)
        print(f'''\nYou have achieved {progress}% of your financial goal for
{category}''')
    else:
        print(f'''There is no financial goal set for {category} or there are \
no transactions in this category.''')


# Function to delete tranaction by transaction ID.
def delete_transaction():
    try:
        trans_id = int(input('''Enter the ID of the transaction to be \
deleted:\n'''))
        cursor.execute('''SELECT * FROM budget_tracker WHERE Trans_ID = \
?''', (trans_id,))
        transaction = cursor.fetchone()
        if transaction is None:
            print(f"Transaction {trans_id} does not exist.")
        else:
            cursor.execute('''DELETE FROM budget_tracker WHERE Trans_ID = \
?''', (trans_id,))
            db.commit()
            print(f"\nTransaction {trans_id} has been successfully deleted.")
    except ValueError:
        print("Invalid transaction ID. Please enter a valid transaction ID.")


# Function to delete tranactions by category.
def delete_transaction_category():
    category = input("Enter category to be delete from the transactions:\n") \
     .lower()
    cursor.execute('''
                SELECT COUNT(*) FROM budget_tracker WHERE Trans_Category = ?
            ''', (category,))
    count = cursor.fetchone()[0]
    if count == 0:
        print(f"The category {category} does not exist in the database.")
    else:
        cursor.execute('''
                DELETE FROM budget_tracker WHERE Trans_Category = ?
            ''', (category,))
        print(f"\nCategory {category} has been successfully deleted.")
    db.commit()


# ----------------------------------------------------------------------
# Dictionary Definition
transaction_dict = {
    1: lambda: add_transaction("expense"),
    2: lambda: transaction_type_view("expense"),
    3: lambda: transaction_category_view(input("Enter expenses category to \
view:\n").lower()),
    4: lambda: add_transaction("income"),
    5: lambda: transaction_type_view("income"),
    6: lambda: transaction_category_view(input("Enter income category to \
view:\n").lower()),
    7: lambda: set_budget(),
    8: lambda: view_budget(),
    9: lambda: set_financial_goal(),
    10: lambda: view_progress(),
    11: lambda: delete_transaction(),
    12: lambda: delete_transaction_category()
}


# ========================= Part 3 =====================================
# Main loop of the Application
while True:
    # Menu of transactions that can be performed is called.
    # User choice is requested.
    transaction_options()
    transaction = get_transaction()

    # Appropriate functions is called if user choice is in the dictionary.
    if transaction in transaction_dict:
        transaction_dict[transaction]()

    # Application is exited if user choice is not in the menu of options.
    else:
        print('''You have elected to exit the application. Goodbye!''')
        break
db.close()
