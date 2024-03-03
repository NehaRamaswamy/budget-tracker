import tkinter as tk
from tkinter import messagebox
import json
import pandas as pd
from openpyxl.workbook import Workbook
class BudgetTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.root.geometry("400x400")

        self.expenses = []
        self.incomes = []

        self.create_widgets()

    def create_widgets(self):
        # Create input fields for expense and income
        tk.Label(self.root, text="Expense Category:").pack()
        self.expense_category = tk.Entry(self.root)
        self.expense_category.pack()

        tk.Label(self.root, text="Expense Amount:").pack()
        self.expense_amount = tk.Entry(self.root)
        self.expense_amount.pack()

        tk.Label(self.root, text="Income Category:").pack()
        self.income_category = tk.Entry(self.root)
        self.income_category.pack()

        tk.Label(self.root, text="Income Amount:").pack()
        self.income_amount = tk.Entry(self.root)
        self.income_amount.pack()


        # Create a button to add expense/income
        tk.Button(self.root, text="Add Expense", command=self.add_expense).pack()
        tk.Button(self.root, text="Income", command=self.add_income).pack()

        # Create a button to calculate budget
        tk.Button(self.root, text="Calculate Budget", command=self.calculate_budget).pack()

        # Create a button to display income list
        tk.Button(self.root, text="Income List", command=self.display_incomes).pack()

        # Create a button to display expense list
        tk.Button(self.root, text="Expense List", command=self.display_expenses).pack()

       # Create a button to save data
        tk.Button(self.root, text="Save Data",  command=self.save_to_excel).pack()

    def save_to_excel(self):
        data = {
            "expenses": [{"category": expense["category"], "amount": expense["amount"]} for expense in self.expenses],
            "incomes": [{"category": income["category"], "amount": income["amount"]} for income in self.incomes],
        }

        expenses_df = pd.DataFrame(data["expenses"])
        incomes_df = pd.DataFrame(data["incomes"])

        with pd.ExcelWriter("budget_data.xlsx") as writer:
            expenses_df.to_excel(writer, sheet_name="expenses", index=False)
            incomes_df.to_excel(writer, sheet_name="incomes", index=False)

    def add_expense(self):
        category = self.expense_category.get()
        amount = float(self.expense_amount.get())

        self.expenses.append({"category": category, "amount": amount})
        self.expense_category.delete(0, tk.END)
        self.expense_amount.delete(0, tk.END)
        self.calculate_budget()

    def add_income(self):
        category = self.income_category.get()
        amount = float(self.income_amount.get())

        self.incomes.append({"category": category, "amount": amount})


        self.income_category.delete(0, tk.END)
        self.income_amount.delete(0, tk.END)
        messagebox.showinfo("Updated Successfully!",f"Added:{amount}")

    def display_expenses(self):
        expense_str = "\n".join([f"{expense['category']}: {expense['amount']}" for expense in self.expenses])
        messagebox.showinfo("Expense List", expense_str)

    def display_incomes(self):
        income_str = "\n".join([f"{income['category']}: {income['amount']}" for income in self.incomes])
        messagebox.showinfo("Income List", income_str)


    def calculate_budget(self):
        total_expenses = sum([expense["amount"] for expense in self.expenses])
        total_incomes = sum([income["amount"] for income in self.incomes])

        remaining_budget = total_incomes - total_expenses

        messagebox.showinfo("Budget Calculation", f"Remaining Budget: {remaining_budget}")

    def save_data(self):
        data = {"expenses": self.expenses, "incomes": self.incomes}

        with open("budget_data.json", "w") as outfile:
            json.dump(data, outfile)

root = tk.Tk()
budget_tracker = BudgetTracker(root)
root.mainloop()