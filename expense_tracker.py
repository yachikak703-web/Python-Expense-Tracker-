import json
import csv
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("expenses.json")
CATEGORIES = ["Food", "Travel", "Shopping", "Education", "Bills", "Health", "Other"]


def load_expenses():
    """Load saved expenses from the JSON file."""
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read expenses.json. Starting with an empty list.")
        return []


def save_expenses(expenses):
    """Save expenses to the JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)


def get_amount():
    while True:
        try:
            amount = float(input("Amount (₹): ").strip())
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Please enter a valid number.")


def add_expense(expenses):
    print("\n--- Add an Expense ---")
    title = input("What did you spend on? ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    print("Categories:", ", ".join(CATEGORIES))
    category = input("Category: ").strip().title()
    if category not in CATEGORIES:
        category = "Other"

    amount = get_amount()
    date_text = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
    if not date_text:
        date_text = datetime.now().strftime("%Y-%m-%d")
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    expense = {
        "id": max((item["id"] for item in expenses), default=0) + 1,
        "title": title,
        "category": category,
        "amount": amount,
        "date": date_text
    }
    expenses.append(expense)
    save_expenses(expenses)
    print("Expense saved successfully!")


def view_expenses(expenses):
    print("\n--- All Expenses ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f'{"ID":<5} {"DATE":<12} {"CATEGORY":<14} {"TITLE":<24} AMOUNT')
    print("-" * 68)
    for item in sorted(expenses, key=lambda x: (x["date"], x["id"])):
        print(f'{item["id"]:<5} {item["date"]:<12} {item["category"]:<14} '
              f'{item["title"][:23]:<24} ₹{item["amount"]:.2f}')


def show_summary(expenses):
    print("\n--- Expense Summary ---")
    if not expenses:
        print("No expenses to summarize.")
        return

    total = sum(item["amount"] for item in expenses)
    print(f"Total spent: ₹{total:.2f}")
    print(f"Number of expenses: {len(expenses)}")
    print("\nSpending by category:")
    totals = {}
    for item in expenses:
        totals[item["category"]] = totals.get(item["category"], 0) + item["amount"]

    for category, amount in sorted(totals.items(), key=lambda pair: pair[1], reverse=True):
        print(f"  {category:<14} ₹{amount:.2f}")


def delete_expense(expenses):
    view_expenses(expenses)
    if not expenses:
        return
    try:
        expense_id = int(input("\nEnter the ID to delete: "))
    except ValueError:
        print("Please enter a valid ID.")
        return

    for item in expenses:
        if item["id"] == expense_id:
            expenses.remove(item)
            save_expenses(expenses)
            print("Expense deleted.")
            return
    print("No expense found with that ID.")


def export_csv(expenses):
    if not expenses:
        print("There are no expenses to export.")
        return

    output_file = Path("expenses_export.csv")
    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "date", "title", "category", "amount"])
        writer.writeheader()
        for item in expenses:
            writer.writerow(item)
    print(f"CSV exported to: {output_file.resolve()}")


def main():
    expenses = load_expenses()
    while True:
        print("\n========== PERSONAL EXPENSE TRACKER ==========")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. View spending summary")
        print("4. Delete an expense")
        print("5. Export expenses to CSV")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            show_summary(expenses)
        elif choice == "4":
            delete_expense(expenses)
        elif choice == "5":
            export_csv(expenses)
        elif choice == "0":
            print("Thank you for using Personal Expense Tracker!")
            break
        else:
            print("Invalid choice. Please select 0 to 5.")


if __name__ == "__main__":
    main()
