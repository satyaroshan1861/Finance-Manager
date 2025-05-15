"""
Personal Finance Tracker

A Python application to help users track their personal finances, analyze spending habits, and plan budgets.
"""
import os
import json
import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import matplotlib.pyplot as plt


@dataclass
class Transaction:
    """Represents a financial transaction."""
    amount: float
    category: str
    description: str
    date: str
    transaction_type: str  # "income" or "expense"
    
    def to_dict(self):
        """Convert transaction to dictionary."""
        return asdict(self)


class FinanceTracker:
    """Main class for tracking finances."""
    
    def __init__(self, data_file="finance_data.json"):
        """Initialize the finance tracker."""
        self.data_file = data_file
        self.transactions = []
        self.load_data()
        
    def load_data(self):
        """Load transaction data from file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.transactions = [Transaction(**t) for t in data]
            except (json.JSONDecodeError, KeyError):
                print("Error loading data file. Starting with empty transactions.")
                self.transactions = []
        else:
            self.transactions = []
    
    def save_data(self):
        """Save transaction data to file."""
        with open(self.data_file, 'w') as f:
            json.dump([t.to_dict() for t in self.transactions], f, indent=2)
    
    def add_transaction(self, amount: float, category: str, description: str, 
                        date: Optional[str] = None, transaction_type: str = "expense"):
        """Add a new transaction."""
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        transaction = Transaction(
            amount=float(amount),
            category=category,
            description=description,
            date=date,
            transaction_type=transaction_type
        )
        
        self.transactions.append(transaction)
        self.save_data()
        return transaction
    
    def get_balance(self):
        """Calculate current balance."""
        income = sum(t.amount for t in self.transactions if t.transaction_type == "income")
        expenses = sum(t.amount for t in self.transactions if t.transaction_type == "expense")
        return income - expenses
    
    def get_transactions_by_category(self, category=None):
        """Get transactions filtered by category."""
        if category:
            return [t for t in self.transactions if t.category == category]
        return self.transactions
    
    def get_spending_by_category(self):
        """Get total spending grouped by category."""
        categories = {}
        for t in self.transactions:
            if t.transaction_type == "expense":
                if t.category not in categories:
                    categories[t.category] = 0
                categories[t.category] += t.amount
        return categories
    
    def visualize_spending(self):
        """Create a pie chart of spending by category."""
        spending = self.get_spending_by_category()
        if not spending:
            print("No expense data to visualize.")
            return
        
        labels = list(spending.keys())
        values = list(spending.values())
        
        plt.figure(figsize=(10, 7))
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title('Spending by Category')
        plt.axis('equal')
        plt.savefig('spending_chart.png')
        plt.close()
        print("Chart saved as 'spending_chart.png'")
    
    def generate_monthly_report(self, year=None, month=None):
        """Generate a monthly financial report."""
        if year is None or month is None:
            now = datetime.datetime.now()
            year = now.year
            month = now.month
        
        # Filter transactions for the specified month
        monthly_transactions = [
            t for t in self.transactions 
            if datetime.datetime.strptime(t.date, "%Y-%m-%d").year == year
            and datetime.datetime.strptime(t.date, "%Y-%m-%d").month == month
        ]
        
        # Calculate totals
        income = sum(t.amount for t in monthly_transactions if t.transaction_type == "income")
        expenses = sum(t.amount for t in monthly_transactions if t.transaction_type == "expense")
        net = income - expenses
        
        # Group expenses by category
        categories = {}
        for t in monthly_transactions:
            if t.transaction_type == "expense":
                if t.category not in categories:
                    categories[t.category] = 0
                categories[t.category] += t.amount
        
        # Generate report
        report = {
            "year": year,
            "month": month,
            "income": income,
            "expenses": expenses,
            "net": net,
            "categories": categories
        }
        
        return report
    
    # TEMP: Clear saved data (run this once)




def main():
    """Main function to demonstrate the finance tracker."""
    tracker = FinanceTracker()

    if not tracker.transactions:
        print("No existing transactions found. You can start adding your income and expenses now!")

    while True:
        print("\n===== Personal Finance Tracker =====")
        print(f"Current Balance: Rs{tracker.get_balance():.2f}")
        print("\n1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. View Spending by Category")
        print("5. Visualize Spending")
        print("6. Generate Monthly Report")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ")

        if choice == '1':
            amount = float(input("Enter amount: Rs"))
            category = input("Enter category: ")
            description = input("Enter description: ")
            date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
            if not date:
                date = None
            tracker.add_transaction(amount, category, description, date, "income")
            print("Income added successfully!")

        elif choice == '2':
            amount = float(input("Enter amount: Rs"))
            category = input("Enter category: ")
            description = input("Enter description: ")
            date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
            if not date:
                date = None
            tracker.add_transaction(amount, category, description, date, "expense")
            print("Expense added successfully!")

        elif choice == '3':
            print("\n----- All Transactions -----")
            for i, t in enumerate(tracker.transactions, 1):
                print(f"{i}. {t.date} | {t.transaction_type.upper()} | Rs{t.amount:.2f} | {t.category} | {t.description}")

        elif choice == '4':
            spending = tracker.get_spending_by_category()
            print("\n----- Spending by Category -----")
            for category, amount in spending.items():
                print(f"{category}: Rs{amount:.2f}")

        elif choice == '5':
            tracker.visualize_spending()

        elif choice == '6':
            year = int(input("Enter year (YYYY): "))
            month = int(input("Enter month (1-12): "))
            report = tracker.generate_monthly_report(year, month)

            print(f"\n----- Monthly Report: {month}/{year} -----")
            print(f"Total Income: Rs{report['income']:.2f}")
            print(f"Total Expenses: Rs{report['expenses']:.2f}")
            print(f"Net: Rs{report['net']:.2f}")
            print("\nExpenses by Category:")
            for category, amount in report['categories'].items():
                print(f"  {category}: Rs{amount:.2f}")

        elif choice == '7':
            print("Thank you for using the Personal Finance Tracker!")
            break

        else:
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    main()
