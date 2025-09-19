from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1> My Finance Tracker</h1><p>It works!</p>"

@app.route('/add-expense', methods=['GET', 'POST'])
def addExpense():
    if request.method == 'POST':
        item = request.form['item']
        amount = request.form['amount']
        return f"Added {item} for {amount} VND"

    return render_template('add-expense.html')

if __name__ == "__main__":
    app.run(debug=True)