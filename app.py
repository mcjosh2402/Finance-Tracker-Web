from flask import Flask, render_template, request
import json
from datetime import datetime
import os

def saveTransaction(item, amount, type):
    # setup file paths and ensure /data/transactions.json exist 
    base_dir = os.path.dirname(os.path.abspath(__file__)) # get the path of this file
    fileName = os.path.join(base_dir, "data", "transactions.json") # create the full path to .../data/transactions.json
    os.makedirs(os.path.dirname(fileName), exist_ok=True) # create above path if not exist

    expense = { # dictionary (similar to c++ map)
        "item": item,
        "amount": float(amount),
        "date": datetime.today().strftime("%Y-%m-%d"), # convert datetime obj to string
        "type": type
    }

    try:
        with open(fileName, "r") as file:
            transactions = json.load(file) # turn json format to dict
    except (FileNotFoundError, json.JSONDecodeError):
        # handle missing file and empty .json
        transactions = []

    transactions.append(expense)
    with open(fileName, "w") as file:
        json.dump(transactions, file, indent=2) # write python dict to json format

def getTransactions():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    fileName = os.path.join(base_dir, "data", "transactions.json")
    os.makedirs(os.path.dirname(fileName), exist_ok=True)

    try:
        with open(fileName, "r") as file:
            transactions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        transactions = []

    return transactions


app = Flask(__name__) # create a webpage named app

@app.route('/') # main landing page
def home():
    return "<h1> My Finance Tracker</h1><p>It works!</p>"

@app.route('/add-transaction', methods=['GET', 'POST']) # add transaction page
def addTransaction():
    if request.method == 'POST':
        # get the submitted form info that fit the dictionary's key
        item = request.form['item']
        amount = request.form['amount']
        type = request.form['type']

        saveTransaction(item, amount, type)
        return f"Added {item} for {amount} VND as {type}" # confirmation

    return render_template('add-transactions.html') # render add-expense.html 

@app.route('/view-transactions', methods=['GET'])
def viewTransaction():

    return render_template('view-transactions.html', transactions = getTransactions())

if __name__ == "__main__":
    app.run(debug=True)