import csv
import os

FILE_NAME = "expenses.csv"

# Create CSV file if it doesn't exist
def create_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Date", "Category", "Amount", "Description"])

# Add Expense
def add_expense():
    date = input("Enter Date (YYYY-MM-DD): ")
    category = input("Enter Category: ")
    amount = float(input("Enter Amount: "))
    description = input("Enter Description: ")

    with open(FILE_NAME, "r") as file:
        rows = list(csv.reader(file))
        expense_id = len(rows)

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([expense_id, date, category, amount, description])

    print("Expense Added Successfully.")

# View Expenses
def view_expenses():
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        print("\nExpense Records")
        print("-" * 60)
        for row in reader:
            print(row)

# Update Expense
def update_expense():
    expense_id = input("Enter Expense ID to Update: ")

    rows = []

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == expense_id:
                row[1] = input("New Date: ")
                row[2] = input("New Category: ")
                row[3] = input("New Amount: ")
                row[4] = input("New Description: ")
            rows.append(row)

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print("Expense Updated.")

# Delete Expense
def delete_expense():
    expense_id = input("Enter Expense ID to Delete: ")

    rows = []

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] != expense_id:
                rows.append(row)

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print("Expense Deleted.")

# Total Expense
def total_expense():
    total = 0

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            total += float(row[3])

    print("Total Expense =", total)

# Monthly Expense
def monthly_expense():
    month = input("Enter Month (YYYY-MM): ")
    total = 0

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if row[1].startswith(month):
                total += float(row[3])

    print("Monthly Expense =", total)

# Main Menu
def menu():
    create_file()

    while True:
        print("\n===== Expense Tracker =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Total Expense")
        print("6. Monthly Expense")
        print("7. Exit")

        choice = input("Enter Choice: ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            update_expense()

        elif choice == "4":
            delete_expense()

        elif choice == "5":
            total_expense()

        elif choice == "6":
            monthly_expense()

        elif choice == "7":
            print("Thank You!")
            break

        else:
            print("Invalid Choice")

menu()
