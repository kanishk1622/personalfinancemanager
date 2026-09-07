from database import Database
from finance import FinanceManager
from datetime import datetime


db = Database()
finance = FinanceManager(db)


def line():
    print("=" * 60)


def pause():
    input("\nPress Enter to continue...")


def get_amount():
    while True:
        try:
            amount = float(input("Enter amount:₹"))

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

            return amount

        except ValueError:
            print("Please enter a valid amount.")


def choose_category():
    print("\nCategories:")

    for i, category in enumerate(FinanceManager.CATEGORIES, 1):
        print(f"{i}. {category}")

    while True:
        try:
            choice = int(input("Choose category: "))

            if 1 <= choice <= len(FinanceManager.CATEGORIES):
                return FinanceManager.CATEGORIES[choice - 1]

            print("Invalid choice.")

        except ValueError:
            print("Enter a number.")


def choose_payment_method():
    print("\nPayment Methods:")

    for i, method in enumerate(FinanceManager.PAYMENT_METHODS, 1):
        print(f"{i}. {method}")

    while True:
        try:
            choice = int(input("Choose payment method: "))

            if 1 <= choice <= len(FinanceManager.PAYMENT_METHODS):
                return FinanceManager.PAYMENT_METHODS[choice - 1]

            print("Invalid choice.")

        except ValueError:
            print("Enter a number.")


def add_income():

    line()
    print("ADD INCOME")
    line()

    amount = get_amount()

    description = input("Description: ")

    payment_method = choose_payment_method()

    transaction_id = finance.add_transaction(
        amount,
        "Income",
        "Income",
        description,
        payment_method
    )

    print(f"\nIncome added successfully!")
    print(f"Transaction ID: {transaction_id}")

    pause()


def add_expense():

    line()
    print("ADD EXPENSE")
    line()

    amount = get_amount()

    category = choose_category()

    description = input("Description: ")

    payment_method = choose_payment_method()

    transaction_id = finance.add_transaction(
        amount,
        "Expense",
        category,
        description,
        payment_method
    )

    print(f"\nExpense added successfully!")
    print(f"Transaction ID: {transaction_id}")

    pause()


def add_investment():

    line()
    print("ADD INVESTMENT")
    line()

    print("\nInvestment Types:")

    for i, investment_type in enumerate(
        FinanceManager.INVESTMENT_TYPES, 1
    ):
        print(f"{i}. {investment_type}")

    while True:
        try:
            choice = int(input("Choose investment type: "))

            if 1 <= choice <= len(FinanceManager.INVESTMENT_TYPES):
                investment_type = FinanceManager.INVESTMENT_TYPES[
                    choice - 1
                ]
                break

            print("Invalid choice.")

        except ValueError:
            print("Enter a number.")

    name = input("Investment name: ")

    amount = get_amount()

    investment_id = finance.add_investment(
        investment_type,
        name,
        amount
    )

    print("\nInvestment added successfully!")
    print(f"Investment ID: {investment_id}")

    pause()


def display_transactions(transactions):

    if not transactions:
        print("\nNo transactions found.")
        return

    line()

    print(
        f"{'ID':<8}"
        f"{'Date':<13}"
        f"{'Amount':<12}"
        f"{'Type':<10}"
        f"{'Category':<16}"
    )

    line()

    for transaction in transactions:

        transaction_id = transaction[0]
        date = transaction[1]
        amount = transaction[2]
        transaction_type = transaction[3]
        category = transaction[4]

        print(
            f"{transaction_id:<8}"
            f"{date:<13}"
            f"₹{amount:<11.2f}"
            f"{transaction_type:<10}"
            f"{category:<16}"
        )

        print(f"        Description: {transaction[5]}")
        print(f"        Payment: {transaction[6]}")

    line()


def view_transactions():

    line()
    print("ALL TRANSACTIONS")
    line()

    transactions = db.get_transactions()

    display_transactions(transactions)

    pause()


def search_transaction():

    line()
    print("SEARCH TRANSACTION")
    line()

    keyword = input(
        "Enter Transaction ID, category, description or payment method: "
    )

    transactions = db.search_transactions(keyword)

    display_transactions(transactions)

    pause()


def delete_transaction():

    line()
    print("DELETE TRANSACTION")
    line()

    transaction_id = input("Enter Transaction ID: ").strip()

    deleted = db.delete_transaction(transaction_id)

    if deleted:
        print("\nTransaction deleted successfully.")
    else:
        print("\nTransaction not found.")

    pause()


def view_balance():

    line()
    print("FINANCIAL OVERVIEW")
    line()

    income = db.get_total_income()
    expense = db.get_total_expense()
    balance = finance.get_balance()
    investment = db.get_total_investment()

    print(f"\nTotal Income       : ₹{income:.2f}")
    print(f"Total Expenses     : ₹{expense:.2f}")
    print(f"Current Balance    : ₹{balance:.2f}")
    print(f"Total Investments  : ₹{investment:.2f}")

    line()

    pause()


def expense_summary():

    line()
    print("EXPENSE SUMMARY")
    line()

    summary = finance.get_category_summary()

    if not summary:
        print("\nNo expenses recorded.")
        pause()
        return

    total = db.get_total_expense()

    print()

    for category, amount in summary:

        percentage = (amount / total) * 100

        print(
            f"{category:<20}"
            f"₹{amount:<12.2f}"
            f"{percentage:.1f}%"
        )

    line()

    pause()


def investment_summary():

    line()
    print("INVESTMENT SUMMARY")
    line()

    investments = db.get_investments()

    if not investments:
        print("\nNo investments recorded.")
        pause()
        return

    print(
        f"{'ID':<8}"
        f"{'Date':<13}"
        f"{'Type':<18}"
        f"{'Name':<20}"
        f"{'Amount':<12}"
    )

    line()

    for investment in investments:

        print(
            f"{investment[0]:<8}"
            f"{investment[1]:<13}"
            f"{investment[2]:<18}"
            f"{investment[3]:<20}"
            f"₹{investment[4]:<11.2f}"
        )

    line()

    print(
        f"\nTotal Invested: ₹{db.get_total_investment():.2f}"
    )

    pause()


def set_budget():

    line()
    print("SET MONTHLY BUDGET")
    line()

    category = choose_category()

    month = input(
        "Enter month (YYYY-MM), e.g. 2026-09: "
    ).strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format.")
        pause()
        return

    amount = get_amount()

    db.add_budget(category, month, amount)

    print("\nBudget saved successfully.")

    pause()


def view_budget():

    line()
    print("MONTHLY BUDGET")
    line()

    month = input(
        "Enter month (YYYY-MM), e.g. 2026-09: "
    ).strip()

    budgets = db.get_budgets(month)

    if not budgets:
        print("\nNo budgets found for this month.")
        pause()
        return

    print()

    for category, budget in budgets:

        spent = db.get_monthly_expense(
            month,
            category
        )

        remaining = budget - spent

        print(f"Category : {category}")
        print(f"Budget   : ₹{budget:.2f}")
        print(f"Spent    : ₹{spent:.2f}")
        print(f"Remaining: ₹{remaining:.2f}")

        if spent > budget:
            print("Status   : OVER BUDGET")
        else:
            print("Status   : Within budget")

        print("-" * 40)

    pause()


def monthly_report():

    line()
    print("MONTHLY REPORT")
    line()

    month = input(
        "Enter month (YYYY-MM), e.g. 2026-09: "
    ).strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format.")
        pause()
        return

    income, expense = finance.get_monthly_report(month)

    print(f"\nMonth: {month}")
    print(f"Income : ₹{income:.2f}")
    print(f"Expense: ₹{expense:.2f}")
    print(f"Savings: ₹{income - expense:.2f}")

    pause()


def main_menu():

    while True:

        line()

        print("           SMART EXPENSE TRACKER")
        line()

        print("1. Add Income")
        print("2. Add Expense")
        print("3. Add Investment")
        print("4. View All Transactions")
        print("5. Search Transaction")
        print("6. Delete Transaction")
        print("7. View Financial Overview")
        print("8. Expense Summary")
        print("9. Investment Summary")
        print("10. Set Monthly Budget")
        print("11. View Budget")
        print("12. Monthly Report")
        print("13. Exit")

        line()

        choice = input("Enter your choice: ")

        if choice == "1":
            add_income()

        elif choice == "2":
            add_expense()

        elif choice == "3":
            add_investment()

        elif choice == "4":
            view_transactions()

        elif choice == "5":
            search_transaction()

        elif choice == "6":
            delete_transaction()

        elif choice == "7":
            view_balance()

        elif choice == "8":
            expense_summary()

        elif choice == "9":
            investment_summary()

        elif choice == "10":
            set_budget()

        elif choice == "11":
            view_budget()

        elif choice == "12":
            monthly_report()

        elif choice == "13":
            print("\nThank you for using Smart Expense Tracker!")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()