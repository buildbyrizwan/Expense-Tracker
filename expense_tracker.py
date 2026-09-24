import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"
MONTHLY_BUDGET_LIMIT = 5000.0


def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])


def add_expense(category, amount, description):
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(FILE_NAME, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])
    print(f"Added: {description} (Rs. {amount}) under '{category}'")

    # Budget threshold check
    with open(FILE_NAME, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header row
        current_total = sum(float(r[2]) for r in reader)

    if current_total > MONTHLY_BUDGET_LIMIT:
        print(
            f"⚠️  WARNING: You have exceeded the monthly budget limit of Rs. {MONTHLY_BUDGET_LIMIT:.2f}! Total spent: Rs. {current_total:.2f}"
        )


def view_expenses():
    if not os.path.exists(FILE_NAME):
        print("No expenses recorded yet.")
        return

    with open(FILE_NAME, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader, None)
        rows = list(reader)

        if not rows:
            print("No expenses found.")
            return

        print("\n" + "=" * 55)
        print(f"{'Date':<18} {'Category':<12} {'Amount (Rs)':<12} {'Description'}")
        print("=" * 55)
        total = 0.0
        for row in rows:
            date, cat, amt, desc = row
            total += float(amt)
            print(f"{date:<18} {cat:<12} {amt:<12} {desc}")
        print("=" * 55)
        print(f"Total Expenditure: Rs. {total:.2f}\n")


def main():
    initialize_file()
    while True:
        print("\n--- Expense Tracker CLI ---")
        print("1. Add Expense")
        print("2. View All Expenses & Summary")
        print("3. Exit")
        choice = input("Enter choice (1-3): ").strip()

        if choice == "1":
            cat = input("Enter Category (Food/Travel/Bills/Misc): ").strip()
            try:
                amt = float(input("Enter Amount: ").strip())
            except ValueError:
                print("Invalid amount. Must be numeric.")
                continue
            desc = input("Enter Description: ").strip()
            add_expense(cat, amt, desc)
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            print("Exiting tracker.")
            break
        else:
            print("Invalid selection. Try again.")


if __name__ == "__main__":
    main()