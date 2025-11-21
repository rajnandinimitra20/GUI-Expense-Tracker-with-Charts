import tkinter as tk
from tkinter import messagebox, ttk
import csv
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

FILE = "expenses.csv"
try:
    with open(FILE, "x", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Amount", "Category", "Description"])
except FileExistsError:
    pass

def add_expense():
    try:
        amount = float(amount_entry.get())
        category = category_entry.get()
        description = description_entry.get()
        date = date_entry.get()
        if not date:
            date = datetime.today().strftime("%Y-%m-%d")

        with open(FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([date, amount, category, description])
        messagebox.showinfo("Success", "Expense Added!")
        amount_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount!")

def view_expenses():
    expenses_window = tk.Toplevel(root)
    expenses_window.title("All Expenses")
    tree = ttk.Treeview(expenses_window, columns=("Date", "Amount", "Category", "Description"), show="headings")
    tree.heading("Date", text="Date")
    tree.heading("Amount", text="Amount")
    tree.heading("Category", text="Category")
    tree.heading("Description", text="Description")
    tree.pack(fill=tk.BOTH, expand=True)

    with open(FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            tree.insert("", tk.END, values=row)

def show_summary():
    totals = defaultdict(float)
    with open(FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            totals[row[2]] += float(row[1])
    
    if not totals:
        messagebox.showinfo("Summary", "No expenses yet!")
        return
    
    # Display pie chart
    categories = list(totals.keys())
    amounts = list(totals.values())
    plt.figure(figsize=(6,6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Expenses by Category")
    plt.show()

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("400x300")

tk.Label(root, text="Amount:").grid(row=0, column=0, padx=10, pady=10)
amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Category:").grid(row=1, column=0, padx=10, pady=10)
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Description:").grid(row=2, column=0, padx=10, pady=10)
description_entry = tk.Entry(root)
description_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=10)
date_entry = tk.Entry(root)
date_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Button(root, text="Add Expense", command=add_expense).grid(row=4, column=0, pady=20)
tk.Button(root, text="View Expenses", command=view_expenses).grid(row=4, column=1, pady=20)
tk.Button(root, text="Summary (Pie Chart)", command=show_summary).grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()

