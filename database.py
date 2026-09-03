import sqlite3


class Database:

    def __init__(self, db_name="expense_tracker.db"):
        self.db_name = db_name
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id TEXT UNIQUE NOT NULL,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                payment_method TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS investments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                investment_id TEXT UNIQUE NOT NULL,
                date TEXT NOT NULL,
                investment_type TEXT NOT NULL,
                name TEXT NOT NULL,
                amount REAL NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                month TEXT NOT NULL,
                amount REAL NOT NULL,
                UNIQUE(category, month)
            )
        """)

        conn.commit()
        conn.close()

    # ---------------- TRANSACTIONS ----------------

    def add_transaction(self, transaction):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO transactions
            (transaction_id, date, amount, type, category,
             description, payment_method)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            transaction.transaction_id,
            transaction.date,
            transaction.amount,
            transaction.type,
            transaction.category,
            transaction.description,
            transaction.payment_method
        ))

        conn.commit()
        conn.close()

    def get_transactions(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT transaction_id, date, amount, type,
                   category, description, payment_method
            FROM transactions
            ORDER BY date DESC, id DESC
        """)

        data = cursor.fetchall()
        conn.close()

        return data

    def search_transactions(self, keyword):
        conn = self.connect()
        cursor = conn.cursor()

        keyword = f"%{keyword}%"

        cursor.execute("""
            SELECT transaction_id, date, amount, type,
                   category, description, payment_method
            FROM transactions
            WHERE transaction_id LIKE ?
               OR category LIKE ?
               OR description LIKE ?
               OR payment_method LIKE ?
            ORDER BY date DESC
        """, (keyword, keyword, keyword, keyword))

        data = cursor.fetchall()
        conn.close()

        return data

    def delete_transaction(self, transaction_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM transactions WHERE transaction_id = ?",
            (transaction_id,)
        )

        deleted = cursor.rowcount

        conn.commit()
        conn.close()

        return deleted > 0

    # ---------------- BALANCE ----------------

    def get_total_income(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE type = 'Income'
        """)

        result = cursor.fetchone()[0]
        conn.close()

        return result

    def get_total_expense(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE type = 'Expense'
        """)

        result = cursor.fetchone()[0]
        conn.close()

        return result

    # ---------------- EXPENSE SUMMARY ----------------

    def get_category_summary(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT category, SUM(amount)
            FROM transactions
            WHERE type = 'Expense'
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """)

        data = cursor.fetchall()
        conn.close()

        return data

    # ---------------- INVESTMENTS ----------------

    def add_investment(self, investment):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO investments
            (investment_id, date, investment_type, name, amount)
            VALUES (?, ?, ?, ?, ?)
        """, (
            investment.investment_id,
            investment.date,
            investment.investment_type,
            investment.name,
            investment.amount
        ))

        conn.commit()
        conn.close()

    def get_investments(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT investment_id, date, investment_type, name, amount
            FROM investments
            ORDER BY date DESC
        """)

        data = cursor.fetchall()
        conn.close()

        return data

    def get_total_investment(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM investments
        """)

        result = cursor.fetchone()[0]
        conn.close()

        return result

    # ---------------- BUDGET ----------------

    def add_budget(self, category, month, amount):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO budgets(category, month, amount)
            VALUES (?, ?, ?)
            ON CONFLICT(category, month)
            DO UPDATE SET amount = excluded.amount
        """, (category, month, amount))

        conn.commit()
        conn.close()

    def get_budgets(self, month):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT category, amount
            FROM budgets
            WHERE month = ?
        """, (month,))

        data = cursor.fetchall()
        conn.close()

        return data

    def get_monthly_expense(self, month, category):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE type = 'Expense'
            AND category = ?
            AND substr(date, 1, 7) = ?
        """, (category, month))

        result = cursor.fetchone()[0]
        conn.close()

        return result