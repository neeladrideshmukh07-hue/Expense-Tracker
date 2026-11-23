
import sqlite3
from datetime import datetime

# --------------------------------
# DATABASE CONNECTION
# --------------------------------

conn = sqlite3.connect("expense_tracker.db")
cursor = conn.cursor()

# Create transaction table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_type TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    description TEXT,
    date TEXT NOT NULL
)
""")

conn.commit()


# --------------------------------
# ADD INCOME
# --------------------------------

def add_income():

    print("\n========== ADD INCOME ==========")

    category = input("Enter income category: ")

    try:
        amount = float(input("Enter income amount: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Invalid amount!")
        return

    description = input("Enter description: ")

    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")

    if date == "":
        date = datetime.now().strftime("%Y-%m-%d")

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format!")
        return

    cursor.execute("""
    INSERT INTO transactions
    (transaction_type, category, amount, description, date)
    VALUES (?, ?, ?, ?, ?)
    """, ("Income", category, amount, description, date))

    conn.commit()

    print("\nIncome added successfully!")


# --------------------------------
# ADD EXPENSE
# --------------------------------

def add_expense():

    print("\n========== ADD EXPENSE ==========")

    print("1. Food")
    print("2. Shopping")
    print("3. Education")
    print("4. Transport")
    print("5. Entertainment")
    print("6. Medical")
    print("7. Other")

    categories = {
        "1": "Food",
        "2": "Shopping",
        "3": "Education",
        "4": "Transport",
        "5": "Entertainment",
        "6": "Medical",
        "7": "Other"
    }

    choice = input("Choose expense category: ")

    if choice not in categories:
        print("Invalid category!")
        return

    category = categories[choice]

    try:
        amount = float(input("Enter expense amount: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Invalid amount!")
        return

    description = input("Enter expense description: ")

    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")

    if date == "":
        date = datetime.now().strftime("%Y-%m-%d")

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format!")
        return

    cursor.execute("""
    INSERT INTO transactions
    (transaction_type, category, amount, description, date)
    VALUES (?, ?, ?, ?, ?)
    """, ("Expense", category, amount, description, date))

    conn.commit()

    print("\nExpense added successfully!")


# --------------------------------
# VIEW ALL TRANSACTIONS
# --------------------------------

def view_transactions():

    print("\n========== ALL TRANSACTIONS ==========")

    cursor.execute("""
    SELECT * FROM transactions ORDER BY date DESC, id DESC
    """)

    records = cursor.fetchall()

    if not records:
        print("No transaction records found.")
        return

    print("-" * 90)

    print(
        f"{'ID':<5}"
        f"{'TYPE':<12}"
        f"{'CATEGORY':<18}"
        f"{'AMOUNT':<12}"
        f"{'DATE':<15}"
        f"{'DESCRIPTION'}"
    )

    print("-" * 90)

    for record in records:

        print(
            f"{record[0]:<5}"
            f"{record[1]:<12}"
            f"{record[2]:<18}"
            f"{record[3]:<12.2f}"
            f"{record[5]:<15}"
            f"{record[4]}"
        )

    print("-" * 90)


# --------------------------------
# CALCULATE FINANCIAL SUMMARY
# --------------------------------

def financial_summary():

    print("\n========== FINANCIAL SUMMARY ==========")

    cursor.execute("""
    SELECT
        COALESCE(SUM(CASE
            WHEN transaction_type = 'Income'
            THEN amount ELSE 0 END), 0),

        COALESCE(SUM(CASE
            WHEN transaction_type = 'Expense'
            THEN amount ELSE 0 END), 0)

    FROM transactions
    """)

    result = cursor.fetchone()

    total_income = result[0]
    total_expense = result[1]

    balance = total_income - total_expense

    print(f"Total Income   : Rs. {total_income:.2f}")
    print(f"Total Expense  : Rs. {total_expense:.2f}")
    print("-" * 40)
    print(f"Remaining Balance: Rs. {balance:.2f}")


# --------------------------------
# DELETE TRANSACTION
# --------------------------------

def delete_transaction():

    print("\n========== DELETE TRANSACTION ==========")

    try:
        transaction_id = int(
            input("Enter transaction ID to delete: ")
        )

    except ValueError:
        print("Please enter a valid ID!")
        return

    cursor.execute(
        "SELECT * FROM transactions WHERE id = ?",
        (transaction_id,)
    )

    record = cursor.fetchone()

    if record is None:
        print("Transaction not found!")
        return

    confirm = input("Are you sure you want to delete? (yes/no): ")

    if confirm.lower() == "yes":

        cursor.execute(
            "DELETE FROM transactions WHERE id = ?",
            (transaction_id,)
        )

        conn.commit()

        print("Transaction deleted successfully!")

    else:
        print("Deletion cancelled.")


# --------------------------------
# MONTHLY EXPENSE REPORT
# --------------------------------

def monthly_report():

    print("\n========== MONTHLY REPORT ==========")

    month = input("Enter month (YYYY-MM): ")

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format!")
        return

    cursor.execute("""
    SELECT
        transaction_type,
        SUM(amount)
    FROM transactions
    WHERE strftime('%Y-%m', date) = ?
    GROUP BY transaction_type
    """, (month,))

    records = cursor.fetchall()

    if not records:
        print("No records found for this month.")
        return

    total_income = 0
    total_expense = 0

    for transaction_type, amount in records:

        if transaction_type == "Income":
            total_income = amount

        elif transaction_type == "Expense":
            total_expense = amount

    print("\nMonth:", month)
    print(f"Total Income : Rs. {total_income:.2f}")
    print(f"Total Expense: Rs. {total_expense:.2f}")
    print(f"Net Balance  : Rs. {total_income - total_expense:.2f}")


# --------------------------------
# MAIN MENU
# --------------------------------

def main():

    while True:

        print("\n")
        print("=" * 45)
        print("       EXPENSE TRACKER MANAGEMENT SYSTEM")
        print("=" * 45)

        print("1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. Financial Summary")
        print("5. Delete Transaction")
        print("6. Monthly Expense Report")
        print("7. Exit")

        print("=" * 45)

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            add_income()

        elif choice == "2":
            add_expense()

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            financial_summary()

        elif choice == "5":
            delete_transaction()

        elif choice == "6":
            monthly_report()

        elif choice == "7":
            print("\nThank you for using Expense Tracker!")
            break

        else:
            print("Invalid choice! Please try again.")


# --------------------------------
# PROGRAM EXECUTION
# --------------------------------

if __name__ == "__main__":

    try:
        main()

    finally:
        conn.close()
