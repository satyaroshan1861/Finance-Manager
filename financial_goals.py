"""
Financial Goals Module

This module allows users to set and track financial goals.
"""
import json
import os
import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from finance_tracker import FinanceTracker


@dataclass
class Goal:
    """Represents a financial goal."""
    name: str
    target_amount: float
    current_amount: float
    deadline: str  # YYYY-MM-DD
    category: str
    description: str
    
    def to_dict(self):
        """Convert goal to dictionary."""
        return asdict(self)
    
    def progress_percentage(self):
        """Calculate progress percentage."""
        if self.target_amount <= 0:
            return 0
        return (self.current_amount / self.target_amount) * 100
    
    def days_remaining(self):
        """Calculate days remaining until deadline."""
        today = datetime.datetime.now().date()
        deadline = datetime.datetime.strptime(self.deadline, "%Y-%m-%d").date()
        return (deadline - today).days


class GoalTracker:
    """Class for tracking financial goals."""
    
    def __init__(self, finance_tracker: FinanceTracker, goals_file="goals.json"):
        """Initialize the goal tracker."""
        self.finance_tracker = finance_tracker
        self.goals_file = goals_file
        self.goals = []
        self.load_goals()
    
    def load_goals(self):
        """Load goals from file."""
        if os.path.exists(self.goals_file):
            try:
                with open(self.goals_file, 'r') as f:
                    data = json.load(f)
                    self.goals = [Goal(**g) for g in data]
            except (json.JSONDecodeError, KeyError):
                print("Error loading goals file. Starting with empty goals.")
                self.goals = []
        else:
            self.goals = []
    
    def save_goals(self):
        """Save goals to file."""
        with open(self.goals_file, 'w') as f:
            json.dump([g.to_dict() for g in self.goals], f, indent=2)
    
    def create_goal(self, name: str, target_amount: float, deadline: str, 
                   category: str, description: str, current_amount: float = 0.0):
        """Create a new financial goal."""
        goal = Goal(
            name=name,
            target_amount=float(target_amount),
            current_amount=float(current_amount),
            deadline=deadline,
            category=category,
            description=description
        )
        
        self.goals.append(goal)
        self.save_goals()
        return goal
    
    def update_goal_progress(self, goal_name: str, amount: float):
        """Update progress towards a goal."""
        for goal in self.goals:
            if goal.name == goal_name:
                goal.current_amount += amount
                self.save_goals()
                return True
        return False
    
    def get_all_goals(self):
        """Get all goals."""
        return self.goals
    
    def get_goal_by_name(self, name: str):
        """Get a goal by name."""
        for goal in self.goals:
            if goal.name == name:
                return goal
        return None
    
    def get_goals_by_category(self, category: str):
        """Get goals by category."""
        return [g for g in self.goals if g.category == category]
    
    def get_goals_summary(self):
        """Get summary of all goals."""
        summary = []
        for goal in self.goals:
            days = goal.days_remaining()
            progress = goal.progress_percentage()
            status = "On Track" if progress >= (100 - days/30*10) else "Behind"
            
            if days < 0:
                status = "Overdue"
            elif progress >= 100:
                status = "Achieved"
            
            summary.append({
                "name": goal.name,
                "progress": progress,
                "days_remaining": days,
                "status": status
            })
        
        return summary


def main():
    """Main function to demonstrate the goal tracker."""
    from finance_tracker import FinanceTracker
    
    tracker = FinanceTracker()
    goal_tracker = GoalTracker(tracker)
    
    # Add sample goals if none exist
    if not goal_tracker.goals:
        print("Adding sample goals...")
        goal_tracker.create_goal(
            "Emergency Fund", 
            10000, 
            (datetime.datetime.now() + datetime.timedelta(days=365)).strftime("%Y-%m-%d"),
            "Savings",
            "Build a 6-month emergency fund",
            2500
        )
        goal_tracker.create_goal(
            "New Car", 
            25000, 
            (datetime.datetime.now() + datetime.timedelta(days=730)).strftime("%Y-%m-%d"),
            "Major Purchase",
            "Save for a new car",
            5000
        )
    
    while True:
        print("\n===== Financial Goals =====")
        print("1. Create New Goal")
        print("2. Update Goal Progress")
        print("3. View All Goals")
        print("4. View Goal Details")
        print("5. Return to Main Menu")
        
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
            
        elif choice == '3':
            goals = goal_tracker.get_all_goals()
            summary = goal_tracker.get_goals_summary()
            
            print("\n----- All Goals -----")
            for i, (goal, summary) in enumerate(zip(goals, summary), 1):
                print(f"{i}. {goal.name}")
                print(f"   Progress: Rs{goal.current_amount:.2f} / Rs{goal.target_amount:.2f} ({summary['progress']:.1f}%)")
                print(f"   Days Remaining: {summary['days_remaining']}")
                print(f"   Status: {summary['status']}")
            
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
            
        elif choice == '5':
            break
            
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
