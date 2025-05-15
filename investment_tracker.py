"""
Investment Tracker Module

This module allows users to track their investments and analyze performance.
"""
import json
import os
import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import matplotlib.pyplot as plt


@dataclass
class Investment:
    """Represents an investment."""
    name: str
    investment_type: str  # stock, bond, mutual fund, etc.
    purchase_date: str
    purchase_price: float
    quantity: float
    current_price: float
    last_updated: str
    
    def to_dict(self):
        """Convert investment to dictionary."""
        return asdict(self)
    
    def current_value(self):
        """Calculate current value of the investment."""
        return self.current_price * self.quantity
    
    def initial_value(self):
        """Calculate initial investment value."""
        return self.purchase_price * self.quantity
    
    def profit_loss(self):
        """Calculate profit or loss."""
        return self.current_value() - self.initial_value()
    
    def profit_loss_percentage(self):
        """Calculate profit or loss percentage."""
        if self.initial_value() == 0:
            return 0
        return (self.profit_loss() / self.initial_value()) * 100


class InvestmentTracker:
    """Class for tracking investments."""
    
    def __init__(self, investments_file="investments.json"):
        """Initialize the investment tracker."""
        self.investments_file = investments_file
        self.investments = []
        self.load_investments()
    
    def load_investments(self):
        """Load investments from file."""
        if os.path.exists(self.investments_file):
            try:
                with open(self.investments_file, 'r') as f:
                    data = json.load(f)
                    self.investments = [Investment(**inv) for inv in data]
            except (json.JSONDecodeError, KeyError):
                print("Error loading investments file. Starting with empty investments.")
                self.investments = []
        else:
            self.investments = []
    
    def save_investments(self):
        """Save investments to file."""
        with open(self.investments_file, 'w') as f:
            json.dump([inv.to_dict() for inv in self.investments], f, indent=2)
    
    def add_investment(self, name: str, investment_type: str, purchase_date: str,
                      purchase_price: float, quantity: float, current_price: float):
        """Add a new investment."""
        investment = Investment(
            name=name,
            investment_type=investment_type,
            purchase_date=purchase_date,
            purchase_price=float(purchase_price),
            quantity=float(quantity),
            current_price=float(current_price),
            last_updated=datetime.datetime.now().strftime("%Y-%m-%d")
        )
        
        self.investments.append(investment)
        self.save_investments()
        return investment
    
    def update_investment_price(self, name: str, new_price: float):
        """Update the current price of an investment."""
        for inv in self.investments:
            if inv.name == name:
                inv.current_price = float(new_price)
                inv.last_updated = datetime.datetime.now().strftime("%Y-%m-%d")
                self.save_investments()
                return True
        return False
    
    def get_all_investments(self):
        """Get all investments."""
        return self.investments
    
    def get_investment_by_name(self, name: str):
        """Get an investment by name."""
        for inv in self.investments:
            if inv.name == name:
                return inv
        return None
    
    def get_investments_by_type(self, investment_type: str):
        """Get investments by type."""
        return [inv for inv in self.investments if inv.investment_type == investment_type]
    
    def get_portfolio_value(self):
        """Calculate total portfolio value."""
        return sum(inv.current_value() for inv in self.investments)
    
    def get_portfolio_profit_loss(self):
        """Calculate total portfolio profit/loss."""
        return sum(inv.profit_loss() for inv in self.investments)
    
    def get_portfolio_allocation(self):
        """Get portfolio allocation by investment type."""
        allocation = {}
        total_value = self.get_portfolio_value()
        
        if total_value == 0:
            return allocation
        
        for inv in self.investments:
            inv_type = inv.investment_type
            if inv_type not in allocation:
                allocation[inv_type] = 0
            allocation[inv_type] += inv.current_value()
        
        # Convert to percentages
        for inv_type in allocation:
            allocation[inv_type] = (allocation[inv_type] / total_value) * 100
        
        return allocation
    
    def visualize_portfolio_allocation(self):
        """Visualize portfolio allocation."""
        allocation = self.get_portfolio_allocation()
        
        if not allocation:
            print("No investment data to visualize.")
            return
        
        labels = list(allocation.keys())
        values = list(allocation.values())
        
        plt.figure(figsize=(10, 7))
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title('Portfolio Allocation by Investment Type')
        plt.axis('equal')
        plt.savefig('portfolio_allocation.png')
        plt.close()
        print("Chart saved as 'portfolio_allocation.png'")


def main():
    """Main function to demonstrate the investment tracker."""
    tracker = InvestmentTracker()
    
    # Add sample investments if none exist
    if not tracker.investments:
        print("Adding sample investments...")
        tracker.add_investment(
            "AAPL", "Stock", "2022-01-15", 150.0, 10, 175.0
        )
        tracker.add_investment(
            "MSFT", "Stock", "2022-02-20", 280.0, 5, 300.0
        )
        tracker.add_investment(
            "VTI", "ETF", "2022-03-10", 200.0, 15, 210.0
        )
    
    while True:
        print("\n===== Investment Tracker =====")
        print(f"Portfolio Value: Rs{tracker.get_portfolio_value():.2f}")
        print(f"Total Profit/Loss: Rs{tracker.get_portfolio_profit_loss():.2f}")
        print("\n1. Add Investment")
        print("2. Update Investment Price")
        print("3. View All Investments")
        print("4. View Investment Details")
        print("5. View Portfolio Allocation")
        print("6. Return to Main Menu")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            name = input("Enter investment name/symbol: ")
            inv_type = input("Enter investment type (Stock, ETF, Bond, etc.): ")
            purchase_date = input("Enter purchase date (YYYY-MM-DD): ")
            purchase_price = float(input("Enter purchase price per unit: Rs"))
            quantity = float(input("Enter quantity: "))
            current_price = float(input("Enter current price per unit: Rs"))
            
            tracker.add_investment(name, inv_type, purchase_date, purchase_price, quantity, current_price)
            print(f"Investment '{name}' added successfully!")
            
        elif choice == '2':
            investments = tracker.get_all_investments()
            print("\n----- Your Investments -----")
            for i, inv in enumerate(investments, 1):
                print(f"{i}. {inv.name} (Current: Rs{inv.current_price:.2f})")
            
            name = input("\nEnter investment name to update: ")
            inv = tracker.get_investment_by_name(name)
            
            if inv:
                new_price = float(input("Enter new price: Rs"))
                tracker.update_investment_price(name, new_price)
                print(f"Investment '{name}' updated successfully!")
            else:
                print("Investment not found.")
            
        elif choice == '3':
            investments = tracker.get_all_investments()
            print("\n----- All Investments -----")
            for i, inv in enumerate(investments, 1):
                profit_loss = inv.profit_loss()
                profit_loss_pct = inv.profit_loss_percentage()
                profit_loss_str = f"+Rs{profit_loss:.2f} (+{profit_loss_pct:.1f}%)" if profit_loss >= 0 else f"-Rs{abs(profit_loss):.2f} ({profit_loss_pct:.1f}%)"
                
                print(f"{i}. {inv.name} ({inv.investment_type})")
                print(f"   Value: Rs{inv.current_value():.2f} | P/L: {profit_loss_str}")
            
        elif choice == '4':
            name = input("Enter investment name: ")
            inv = tracker.get_investment_by_name(name)
            
            if inv:
                profit_loss = inv.profit_loss()
                profit_loss_pct = inv.profit_loss_percentage()
                
                print(f"\n----- {inv.name} ({inv.investment_type}) -----")
                print(f"Purchase Date: {inv.purchase_date}")
                print(f"Purchase Price: Rs{inv.purchase_price:.2f}")
                print(f"Current Price: Rs{inv.current_price:.2f}")
                print(f"Quantity: {inv.quantity}")
                print(f"Initial Investment: Rs{inv.initial_value():.2f}")
                print(f"Current Value: Rs{inv.current_value():.2f}")
                print(f"Profit/Loss: Rs{profit_loss:.2f} ({profit_loss_pct:.1f}%)")
                print(f"Last Updated: {inv.last_updated}")
            else:
                print("Investment not found.")
            
        elif choice == '5':
            tracker.visualize_portfolio_allocation()
            
        elif choice == '6':
            break
            
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
