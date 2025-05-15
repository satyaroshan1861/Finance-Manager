"""
Financial Analysis Module

This module provides advanced financial analysis capabilities for the finance tracker.
"""
import datetime
import calendar
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Optional
from finance_tracker import FinanceTracker, Transaction


class FinancialAnalysis:
    """Class for analyzing financial data."""
    
    def __init__(self, finance_tracker: FinanceTracker):
        """Initialize the financial analysis."""
        self.finance_tracker = finance_tracker
    
    def monthly_income_vs_expenses(self, year=None):
        """Analyze monthly income vs expenses for a given year."""
        if year is None:
            year = datetime.datetime.now().year
        
        # Initialize data structures
        months = range(1, 13)
        income_by_month = {m: 0 for m in months}
        expenses_by_month = {m: 0 for m in months}
        
        # Categorize transactions by month
        for transaction in self.finance_tracker.transactions:
            date = datetime.datetime.strptime(transaction.date, "%Y-%m-%d")
            if date.year == year and date.month in months:
                if transaction.transaction_type == "income":
                    income_by_month[date.month] += transaction.amount
                else:  # expense
                    expenses_by_month[date.month] += transaction.amount
        
        return {
            "months": list(calendar.month_abbr)[1:],
            "income": [income_by_month[m] for m in months],
            "expenses": [expenses_by_month[m] for m in months]
        }
    
    def category_trend_analysis(self, category: str, months: int = 6):
        """Analyze spending trend for a specific category over recent months."""
        today = datetime.datetime.now()
        
        # Calculate date range
        end_date = datetime.datetime(today.year, today.month, 1)
        start_date = end_date
        for _ in range(months):
            # Move to previous month
            if start_date.month == 1:
                start_date = datetime.datetime(start_date.year - 1, 12, 1)
            else:
                start_date = datetime.datetime(start_date.year, start_date.month - 1, 1)
        
        # Initialize data structures
        month_labels = []
        spending = []
        
        # Analyze each month
        current_date = start_date
        while current_date <= end_date:
            year = current_date.year
            month = current_date.month
            
            # Get month label
            month_label = f"{calendar.month_abbr[month]} {year}"
            month_labels.append(month_label)
            
            # Calculate spending for this category in this month
            monthly_spending = sum(
                t.amount for t in self.finance_tracker.transactions
                if t.transaction_type == "expense"
                and t.category == category
                and datetime.datetime.strptime(t.date, "%Y-%m-%d").year == year
                and datetime.datetime.strptime(t.date, "%Y-%m-%d").month == month
            )
            
            spending.append(monthly_spending)
            
            # Move to next month
            if current_date.month == 12:
                current_date = datetime.datetime(current_date.year + 1, 1, 1)
            else:
                current_date = datetime.datetime(current_date.year, current_date.month + 1, 1)
        
        return {
            "category": category,
            "months": month_labels,
            "spending": spending
        }
    
    def savings_rate_analysis(self, months: int = 12):
        """Calculate savings rate over time."""
        today = datetime.datetime.now()
        
        # Calculate date range
        end_date = datetime.datetime(today.year, today.month, 1)
        start_date = end_date
        for _ in range(months - 1):
            # Move to previous month
            if start_date.month == 1:
                start_date = datetime.datetime(start_date.year - 1, 12, 1)
            else:
                start_date = datetime.datetime(start_date.year, start_date.month - 1, 1)
        
        # Initialize data structures
        month_labels = []
        savings_rates = []
        
        # Analyze each month
        current_date = start_date
        while current_date <= end_date:
            year = current_date.year
            month = current_date.month
            
            # Get month label
            month_label = f"{calendar.month_abbr[month]} {year}"
            month_labels.append(month_label)
            
            # Calculate income and expenses for this month
            monthly_income = sum(
                t.amount for t in self.finance_tracker.transactions
                if t.transaction_type == "income"
                and datetime.datetime.strptime(t.date, "%Y-%m-%d").year == year
                and datetime.datetime.strptime(t.date, "%Y-%m-%d").month == month
            )
            
            monthly_expenses = sum(
                t.amount for t in self.finance_tracker.transactions
                if t.transaction_type == "expense"
                and datetime.datetime.strptime(t.date, "%Y-%m-%d").year == year
                and datetime.datetime.strptime(t.date, "%Y-%m-%d").month == month
            )
            
            # Calculate savings rate
            if monthly_income > 0:
                savings_rate = ((monthly_income - monthly_expenses) / monthly_income) * 100
            else:
                savings_rate = 0
            
            savings_rates.append(savings_rate)
            
            # Move to next month
            if current_date.month == 12:
                current_date = datetime.datetime(current_date.year + 1, 1, 1)
            else:
                current_date = datetime.datetime(current_date.year, current_date.month + 1, 1)
        
        return {
            "months": month_labels,
            "savings_rates": savings_rates
        }
    
    def visualize_income_vs_expenses(self, year=None):
        """Visualize monthly income vs expenses."""
        data = self.monthly_income_vs_expenses(year)
        
        months = data["months"]
        income = data["income"]
        expenses = data["expenses"]
        
        x = np.arange(len(months))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(12, 6))
        rects1 = ax.bar(x - width/2, income, width, label='Income')
        rects2 = ax.bar(x + width/2, expenses, width, label='Expenses')
        
        ax.set_title(f'Monthly Income vs Expenses ({year})')
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount (Rs)')
        ax.set_xticks(x)
        ax.set_xticklabels(months)
        ax.legend()
        
        # Add net savings/deficit
        for i in range(len(months)):
            net = income[i] - expenses[i]
            color = 'green' if net >= 0 else 'red'
            ax.annotate(f'Rs{net:.0f}', 
                        xy=(i, max(income[i], expenses[i]) + 50),
                        ha='center', va='bottom',
                        color=color)
        
        plt.tight_layout()
        plt.savefig('income_vs_expenses.png')
        plt.close()
        print("Chart saved as 'income_vs_expenses.png'")
    
    def visualize_category_trend(self, category: str, months: int = 6):
        """Visualize spending trend for a specific category."""
        data = self.category_trend_analysis(category, months)
        
        plt.figure(figsize=(10, 6))
        plt.plot(data["months"], data["spending"], marker='o', linestyle='-')
        plt.title(f'Spending Trend: {category}')
        plt.xlabel('Month')
        plt.ylabel('Amount (Rs)')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        filename = f'trend_{category.lower().replace(" ", "_")}.png'
        plt.savefig(filename)
        plt.close()
        print(f"Chart saved as '{filename}'")
    
    def visualize_savings_rate(self, months: int = 12):
        """Visualize savings rate over time."""
        data = self.savings_rate_analysis(months)
        
        plt.figure(figsize=(10, 6))
        plt.plot(data["months"], data["savings_rates"], marker='o', linestyle='-')
        plt.title('Monthly Savings Rate')
        plt.xlabel('Month')
        plt.ylabel('Savings Rate (%)')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.axhline(y=20, color='r', linestyle='--', alpha=0.7, label='Target (20%)')
        plt.legend()
        plt.tight_layout()
        
        plt.savefig('savings_rate.png')
        plt.close()
        print("Chart saved as 'savings_rate.png'")


def main():
    """Main function to demonstrate the financial analysis."""
    from finance_tracker import FinanceTracker
    
    tracker = FinanceTracker()
    analysis = FinancialAnalysis(tracker)
    
    while True:
        print("\n===== Financial Analysis =====")
        print("1. Income vs Expenses Analysis")
        print("2. Category Trend Analysis")
        print("3. Savings Rate Analysis")
        print("4. Return to Main Menu")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            year = int(input("Enter year to analyze (YYYY): ") or datetime.datetime.now().year)
            analysis.visualize_income_vs_expenses(year)
            
        elif choice == '2':
            categories = set(t.category for t in tracker.transactions if t.transaction_type == "expense")
            print("\nAvailable categories:")
            for i, category in enumerate(categories, 1):
                print(f"{i}. {category}")
            
            category = input("\nEnter category to analyze: ")
            if category in categories:
                months = int(input("Enter number of months to analyze: ") or 6)
                analysis.visualize_category_trend(category, months)
            else:
                print("Invalid category.")
            
        elif choice == '3':
            months = int(input("Enter number of months to analyze: ") or 12)
            analysis.visualize_savings_rate(months)
            
        elif choice == '4':
            break
            
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
