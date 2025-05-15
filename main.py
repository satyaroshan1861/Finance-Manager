"""
Personal Finance Management System

Main application that integrates all modules of the finance management system.
"""
import os
import sys
from finance_tracker import FinanceTracker
from budget_planner import BudgetPlanner
from financial_analysis import FinancialAnalysis
from financial_goals import GoalTracker
from investment_tracker import InvestmentTracker


def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print application header."""
    print("=" * 50)
    print("           PERSONAL FINANCE MANAGER")
    print("=" * 50)


def main_menu():
    """Display the main menu and handle user interaction."""
    # Initialize components
    tracker = FinanceTracker()
    planner = BudgetPlanner(tracker)
    analysis = FinancialAnalysis(tracker)
    goal_tracker = GoalTracker(tracker)
    investment_tracker = InvestmentTracker()
    
    while True:
        clear_screen()
        print_header()
        print(f"\nCurrent Balance: Rs{tracker.get_balance():.2f}")
        
        print("\nMAIN MENU:")
        print("1. Transaction Management")
        print("2. Budget Planning")
        print("3. Financial Analysis")
        print("4. Financial Goals")
        print("5. Investment Tracker")
        print("6. Settings")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            transaction_menu(tracker)
        elif choice == '2':
            budget_menu(planner)
        elif choice == '3':
            analysis_menu(analysis)
        elif choice == '4':
            goal_menu(goal_tracker)
        elif choice == '5':
            investment_menu(investment_tracker)
        elif choice == '6':
            settings_menu(tracker)
        elif choice == '7':
            print("\nThank you for using the Personal Finance Manager!")
            sys.exit(0)
        else:
            input("Invalid choice. Press Enter to continue...")


def transaction_menu(tracker):
    """Handle transaction management."""
    while True:
        clear_screen()
        print_header()
        print("\nTRANSACTION MANAGEMENT")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. View Transactions by Category")
        print("5. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            amount = float(input("Enter amount: Rs"))
            category = input("Enter category: ")
            description = input("Enter description: ")
            date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
            if not date:
                date = None
            tracker.add_transaction(amount, category, description, date, "income")
            print("Income added successfully!")
            input("Press Enter to continue...")
            
        elif choice == '2':
            amount = float(input("Enter amount: Rs"))
            category = input("Enter category: ")
            description = input("Enter description: ")
            date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
            if not date:
                date = None
            tracker.add_transaction(amount, category, description, date, "expense")
            print("Expense added successfully!")
            input("Press Enter to continue...")
            
        elif choice == '3':
            print("\n----- All Transactions -----")
            for i, t in enumerate(tracker.transactions, 1):
                print(f"{i}. {t.date} | {t.transaction_type.upper()} | Rs{t.amount:.2f} | {t.category} | {t.description}")
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            categories = set(t.category for t in tracker.transactions)
            print("\nAvailable categories:")
            for i, category in enumerate(categories, 1):
                print(f"{i}. {category}")
            
            category = input("\nEnter category to view: ")
            if category in categories:
                transactions = tracker.get_transactions_by_category(category)
                print(f"\n----- Transactions in {category} -----")
                for i, t in enumerate(transactions, 1):
                    print(f"{i}. {t.date} | {t.transaction_type.upper()} | Rs{t.amount:.2f} | {t.description}")
            else:
                print("Invalid category.")
            input("\nPress Enter to continue...")
            
        elif choice == '5':
            return
            
        else:
            input("Invalid choice. Press Enter to continue...")


def budget_menu(planner):
    """Handle budget planning."""
    while True:
        clear_screen()
        print_header()
        print("\nBUDGET PLANNING")
        print("1. Create Budget")
        print("2. View All Budgets")
        print("3. Check Budget Status")
        print("4. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            category = input("Enter category: ")
            amount = float(input("Enter budget amount: Rs"))
            period = input("Enter period (monthly/weekly): ")
            planner.create_budget(category, amount, period)
            print(f"Budget for {category} created successfully!")
            input("Press Enter to continue...")
            
        elif choice == '2':
            budgets = planner.get_all_budgets()
            print("\n----- All Budgets -----")
            for i, b in enumerate(budgets, 1):
                print(f"{i}. {b.category}: Rs{b.amount:.2f} ({b.period})")
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            status = planner.calculate_budget_status()
            print("\n----- Budget Status -----")
            for category, data in status.items():
                print(f"{category}:")
                print(f"  Budget: Rs{data['budget']:.2f}")
                print(f"  Spent: Rs{data['spent']:.2f}")
                print(f"  Remaining: Rs{data['remaining']:.2f}")
                print(f"  Used: {data['percentage']:.1f}%")
            input("\nPress Enter to continue...")
                
        elif choice == '4':
            return
            
        else:
            input("Invalid choice. Press Enter to continue...")


def analysis_menu(analysis):
    """Handle financial analysis."""
    while True:
        clear_screen()
        print_header()
        print("\nFINANCIAL ANALYSIS")
        print("1. Income vs Expenses Analysis")
        print("2. Category Trend Analysis")
        print("3. Savings Rate Analysis")
        print("4. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            import datetime
            year = int(input("Enter year to analyze (YYYY): ") or datetime.datetime.now().year)
            analysis.visualize_income_vs_expenses(year)
            input("Press Enter to continue...")
            
        elif choice == '2':
            categories = set(t.category for t in analysis.finance_tracker.transactions if t.transaction_type == "expense")
            print("\nAvailable categories:")
            for i, category in enumerate(categories, 1):
                print(f"{i}. {category}")
            
            category = input("\nEnter category to analyze: ")
            if category in categories:
                months = int(input("Enter number of months to analyze: ") or 6)
                analysis.visualize_category_trend(category, months)
            else:
                print("Invalid category.")
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            months = int(input("Enter number of months to analyze: ") or 12)
            analysis.visualize_savings_rate(months)
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            return
            
        else:
            input("Invalid choice. Press Enter to continue...")


def goal_menu(goal_tracker):
    """Handle financial goals."""
    while True:
        clear_screen()
        print_header()
        print("\nFINANCIAL GOALS")
        print("1. Create New Goal")
        print("2. Update Goal Progress")
        print("3. View All Goals")
        print("4. View Goal Details")
        print("5. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            name = input("Enter goal name: ")
            target = float(input("Enter target amount: Rs"))
            deadline = input("Enter deadline (YYYY-MM-DD): ")
            category = input("Enter category: ")
            description = input("Enter description: ")
            current = float(input("Enter current amount: Rs") or "0")
            
            goal_tracker.create_goal(name, target, deadline, category, description, current)
            print(f"Goal '{name}' created successfully!")
            input("Press Enter to continue...")
            
        elif choice == '2':
            goals = goal_tracker.get_all_goals()
            print("\n----- Your Goals -----")
            for i, g in enumerate(goals, 1):
                print(f"{i}. {g.name} (Rs{g.current_amount:.2f} / Rs{g.target_amount:.2f})")
            
            name = input("\nEnter goal name to update: ")
            goal = goal_tracker.get_goal_by_name(name)
            
            if goal:
                amount = float(input("Enter amount to add: Rs"))
                goal_tracker.update_goal_progress(name, amount)
                print(f"Goal '{name}' updated successfully!")
            else:
                print("Goal not found.")
            input("Press Enter to continue...")
            
        elif choice == '3':
            goals = goal_tracker.get_all_goals()
            summary = goal_tracker.get_goals_summary()
            
            print("\n----- All Goals -----")
            for i, (goal, summary) in enumerate(zip(goals, summary), 1):
                print(f"{i}. {goal.name}")
                print(f"   Progress: Rs{goal.current_amount:.2f} / Rs{goal.target_amount:.2f} ({summary['progress']:.1f}%)")
                print(f"   Days Remaining: {summary['days_remaining']}")
                print(f"   Status: {summary['status']}")
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            name = input("Enter goal name: ")
            goal = goal_tracker.get_goal_by_name(name)
            
            if goal:
                progress = goal.progress_percentage()
                days = goal.days_remaining()
                
                print(f"\n----- {goal.name} -----")
                print(f"Target: Rs{goal.target_amount:.2f}")
                print(f"Current: Rs{goal.current_amount:.2f}")
                print(f"Progress: {progress:.1f}%")
                print(f"Deadline: {goal.deadline} ({days} days remaining)")
                print(f"Category: {goal.category}")
                print(f"Description: {goal.description}")
            else:
                print("Goal not found.")
            input("Press Enter to continue...")
            
        elif choice == '5':
            return
            
        else:
            input("Invalid choice. Press Enter to continue...")


def investment_menu(investment_tracker):
    """Handle investment tracking."""
    while True:
        clear_screen()
        print_header()
        print("\nINVESTMENT TRACKER")
        print(f"Portfolio Value: Rs{investment_tracker.get_portfolio_value():.2f}")
        print(f"Total Profit/Loss: Rs{investment_tracker.get_portfolio_profit_loss():.2f}")
        print("\n1. Add Investment")
        print("2. Update Investment Price")
        print("3. View All Investments")
        print("4. View Investment Details")
        print("5. View Portfolio Allocation")
        print("6. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            name = input("Enter investment name/symbol: ")
            inv_type = input("Enter investment type (Stock, ETF, Bond, etc.): ")
            purchase_date = input("Enter purchase date (YYYY-MM-DD): ")
            purchase_price = float(input("Enter purchase price per unit: Rs"))
            quantity = float(input("Enter quantity: "))
            current_price = float(input("Enter current price per unit: Rs"))
            
            investment_tracker.add_investment(name, inv_type, purchase_date, purchase_price, quantity, current_price)
            print(f"Investment '{name}' added successfully!")
            input("Press Enter to continue...")
            
        elif choice == '2':
            investments = investment_tracker.get_all_investments()
            print("\n----- Your Investments -----")
            for i, inv in enumerate(investments, 1):
                print(f"{i}. {inv.name} (Current: Rs{inv.current_price:.2f})")
            
            name = input("\nEnter investment name to update: ")
            inv = investment_tracker.get_investment_by_name(name)
            
            if inv:
                new_price = float(input("Enter new price: Rs"))
                investment_tracker.update_investment_price(name, new_price)
                print(f"Investment '{name}' updated successfully!")
            else:
                print("Investment not found.")
            input("Press Enter to continue...")
            
        elif choice == '3':
            investments = investment_tracker.get_all_investments()
            print("\n----- All Investments -----")
            for i, inv in enumerate(investments, 1):
                profit_loss = inv.profit_loss()
                profit_loss_pct = inv.profit_loss_percentage()
                profit_loss_str = f"+Rs{profit_loss:.2f} (+{profit_loss_pct:.1f}%)" if profit_loss >= 0 else f"-Rs{abs(profit_loss):.2f} ({profit_loss_pct:.1f}%)"
                
                print(f"{i}. {inv.name} ({inv.investment_type})")
                print(f"   Value: Rs{inv.current_value():.2f} | P/L: {profit_loss_str}")
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            name = input("Enter investment name: ")
            inv = investment_tracker.get_investment_by_name(name)
            
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
            input("\nPress Enter to continue...")
            
        elif choice == '5':
            investment_tracker.visualize_portfolio_allocation()
            input("\nPress Enter to continue...")
            
        elif choice == '6':
            return
            
        else:
            input("Invalid choice. Press Enter to continue...")


def settings_menu(tracker):
    """Handle application settings."""
    while True:
        clear_screen()
        print_header()
        print("\nSETTINGS")
        print("1. Export Data")
        print("2. Import Data")
        print("3. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            print("Data is automatically saved to:")
            print(f"- Transactions: {tracker.data_file}")
            print("- Budgets: budgets.json")
            print("- Goals: goals.json")
            print("- Investments: investments.json")
            input("Press Enter to continue...")
            
        elif choice == '2':
            print("Data import functionality not implemented yet.")
            input("Press Enter to continue...")
            
        elif choice == '3':
            return
            
        else:
            input("Invalid choice. Press Enter to continue...")


if __name__ == "__main__":
    main_menu()
