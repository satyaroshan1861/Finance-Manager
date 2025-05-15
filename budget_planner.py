"""
Budget Planner Module

This module extends the finance tracker with budget planning capabilities.
"""
import json
import os
import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from finance_tracker import FinanceTracker


@dataclass
class Budget:
    """Represents a budget for a specific category."""
    category: str
    amount: float
    period: str  # "monthly", "weekly", etc.
    start_date: str
    end_date: Optional[str] = None
    
    def to_dict(self):
        """Convert budget to dictionary."""
        return asdict(self)


class BudgetPlanner:
    """Class for planning and tracking budgets."""
    
    def __init__(self, finance_tracker: FinanceTracker, budget_file="budgets.json"):
        """Initialize the budget planner."""
        self.finance_tracker = finance_tracker
        self.budget_file = budget_file
        self.budgets = []
        self.load_budgets()
    
    def load_budgets(self):
        """Load budget data from file."""
        if os.path.exists(self.budget_file):
            try:
                with open(self.budget_file, 'r') as f:
                    data = json.load(f)
                    self.budgets = [Budget(**b) for b in data]
            except (json.JSONDecodeError, KeyError):
                print("Error loading budget file. Starting with empty budgets.")
                self.budgets = []
        else:
            self.budgets = []
    
    def save_budgets(self):
        """Save budget data to file."""
        with open(self.budget_file, 'w') as f:
            json.dump([b.to_dict() for b in self.budgets], f, indent=2)
    
    def create_budget(self, category: str, amount: float, period: str, 
                     start_date: Optional[str] = None, end_date: Optional[str] = None):
        """Create a new budget."""
        if start_date is None:
            start_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        budget = Budget(
            category=category,
            amount=float(amount),
            period=period,
            start_date=start_date,
            end_date=end_date
        )
        
        # Remove any existing budget for the same category and period
        self.budgets = [b for b in self.budgets if not (b.category == category and b.period == period)]
        
        self.budgets.append(budget)
        self.save_budgets()
        return budget
    
    def get_budget(self, category: str, period: str = "monthly"):
        """Get budget for a specific category and period."""
        for budget in self.budgets:
            if budget.category == category and budget.period == period:
                return budget
        return None
    
    def get_all_budgets(self):
        """Get all budgets."""
        return self.budgets
    
    def calculate_budget_status(self, year=None, month=None):
        """Calculate budget status for the current month."""
        if year is None or month is None:
            now = datetime.datetime.now()
            year = now.year
            month = now.month
        
        # Get monthly spending by category
        monthly_transactions = [
            t for t in self.finance_tracker.transactions 
            if t.transaction_type == "expense"
            and datetime.datetime.strptime(t.date, "%Y-%m-%d").year == year
            and datetime.datetime.strptime(t.date, "%Y-%m-%d").month == month
        ]
        
        spending_by_category = {}
        for t in monthly_transactions:
            if t.category not in spending_by_category:
                spending_by_category[t.category] = 0
            spending_by_category[t.category] += t.amount
        
        # Compare with budgets
        budget_status = {}
        for budget in self.budgets:
            if budget.period == "monthly":
                category = budget.category
                budget_amount = budget.amount
                spent = spending_by_category.get(category, 0)
                remaining = budget_amount - spent
                percentage = (spent / budget_amount) * 100 if budget_amount > 0 else 0
                
                budget_status[category] = {
                    "budget": budget_amount,
                    "spent": spent,
                    "remaining": remaining,
                    "percentage": percentage
                }
        
        return budget_status


def main():
    """Main function to demonstrate the budget planner."""
    from finance_tracker import FinanceTracker
    
    tracker = FinanceTracker()
    planner = BudgetPlanner(tracker)
    
    # Add sample budgets if none exist
    if not planner.budgets:
        print("Adding sample budgets...")
        planner.create_budget("Groceries", 300, "monthly")
        planner.create_budget("Dining", 150, "monthly")
        planner.create_budget("Entertainment", 200, "monthly")
        planner.create_budget("Utilities", 250, "monthly")
    
    while True:
        print("\n===== Budget Planner =====")
        print("1. Create Budget")
        print("2. View All Budgets")
        print("3. Check Budget Status")
        print("4. Return to Main Menu")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            category = input("Enter category: ")
            amount = float(input("Enter budget amount: Rs"))
            period = input("Enter period (monthly/weekly): ")
            planner.create_budget(category, amount, period)
            print(f"Budget for {category} created successfully!")
            
        elif choice == '2':
            budgets = planner.get_all_budgets()
            print("\n----- All Budgets -----")
            for i, b in enumerate(budgets, 1):
                print(f"{i}. {b.category}: Rs{b.amount:.2f} ({b.period})")
            
        elif choice == '3':
            status = planner.calculate_budget_status()
            print("\n----- Budget Status -----")
            for category, data in status.items():
                print(f"{category}:")
                print(f"  Budget: Rs{data['budget']:.2f}")
                print(f"  Spent: Rs{data['spent']:.2f}")
                print(f"  Remaining: Rs{data['remaining']:.2f}")
                print(f"  Used: {data['percentage']:.1f}%")
                
        elif choice == '4':
            break
            
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
