from datetime import datetime


class Transaction:

    def __init__(
        self,
        transaction_id,
        date,
        amount,
        transaction_type,
        category,
        description,
        payment_method
    ):
        self.transaction_id = transaction_id
        self.date = date
        self.amount = amount
        self.type = transaction_type
        self.category = category
        self.description = description
        self.payment_method = payment_method


class Investment:

    def __init__(
        self,
        investment_id,
        date,
        investment_type,
        name,
        amount
    ):
        self.investment_id = investment_id
        self.date = date
        self.investment_type = investment_type
        self.name = name
        self.amount = amount


class FinanceManager:

    CATEGORIES = [
        "Food",
        "Transport",
        "Shopping",
        "Entertainment",
        "Bills",
        "Education",
        "Health",
        "Travel",
        "Other"
    ]

    PAYMENT_METHODS = [
    "Cash",
    "Bank Account"
]

    INVESTMENT_TYPES = [
        "Stock",
        "Mutual Fund",
        "Fixed Deposit",
        "Gold",
        "Crypto",
        "Other"
    ]

    def __init__(self, database):
        self.db = database

    def generate_transaction_id(self):
        transactions = self.db.get_transactions()

        number = len(transactions) + 1

        while True:
            transaction_id = f"T{number:04d}"

            exists = any(
                transaction[0] == transaction_id
                for transaction in transactions
            )

            if not exists:
                return transaction_id

            number += 1

    def generate_investment_id(self):
        investments = self.db.get_investments()

        number = len(investments) + 1

        while True:
            investment_id = f"I{number:04d}"

            exists = any(
                investment[0] == investment_id
                for investment in investments
            )

            if not exists:
                return investment_id

            number += 1

    def add_transaction(
        self,
        amount,
        transaction_type,
        category,
        description,
        payment_method,
        date=None
    ):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        transaction_id = self.generate_transaction_id()

        transaction = Transaction(
            transaction_id,
            date,
            amount,
            transaction_type,
            category,
            description,
            payment_method
        )

        self.db.add_transaction(transaction)

        return transaction_id

    def add_investment(
        self,
        investment_type,
        name,
        amount,
        date=None
    ):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        investment_id = self.generate_investment_id()

        investment = Investment(
            investment_id,
            date,
            investment_type,
            name,
            amount
        )

        self.db.add_investment(investment)

        return investment_id

    def get_balance(self):
        income = self.db.get_total_income()
        expense = self.db.get_total_expense()

        return income - expense

    def get_savings(self):
        return self.get_balance()

    def get_category_summary(self):
        return self.db.get_category_summary()

    def get_monthly_report(self, month):
        transactions = self.db.get_transactions()

        income = 0
        expense = 0

        for transaction in transactions:

            date = transaction[1]
            amount = transaction[2]
            transaction_type = transaction[3]

            if date.startswith(month):

                if transaction_type == "Income":
                    income += amount

                elif transaction_type == "Expense":
                    expense += amount

        return income, expense