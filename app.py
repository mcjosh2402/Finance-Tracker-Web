from flask import Flask, render_template, request
import json
from datetime import datetime
import os

def saveExpense(item, amount):
    # setup file paths and ensure /data/transactions.json exist 
    base_dir = os.path.dirname(os.path.abspath(__file__)) # get the path of this file
    fileName = os.path.join(base_dir, "data", "transactions.json") # create the full path to .../data/transactions.json
    os.makedirs(os.path.dirname(fileName), exist_ok=True) # create above path if not exist

    expense = { # dictionary (similar to c++ map)
        "item": item,
        "amount": float(amount),
        "date": datetime.today().strftime("%Y-%m-%d"),
        "type": "Expense"
    }

    try:
        # Read existing transactions from JSON file
        with open(fileName, "r") as file:
            transactions = json.load(file)
    except FileNotFoundError:
        # Create empty list if file doesn't exist yet
        transactions = []

    # Append new expense and save back to JSON file
    transactions.append(expense)
    with open(fileName, "w") as file:
        json.dump(transactions, file, indent=2) 

app = Flask(__name__) # create a webpage named app

@app.route('/')
def home():
    return "<h1> My Finance Tracker</h1><p>It works!</p>"

@app.route('/add-expense', methods=['GET', 'POST'])
def addExpense():
    if request.method == 'POST':
        item = request.form['item']
        amount = request.form['amount']

        saveExpense(item, amount)
        return f"Added {item} for {amount} VND"

    return render_template('add-expense.html')

if __name__ == "__main__":
    app.run(debug=True)