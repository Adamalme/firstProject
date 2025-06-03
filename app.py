from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import csv
from io import StringIO
from datetime import datetime

app = Flask(__name__)

DB_NAME = 'transactions.db'


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY,
                        date TEXT,
                        type TEXT,
                        category TEXT,
                        amount REAL,
                        description TEXT
                    )''')
        conn.commit()


@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM transactions ORDER BY date DESC")
        transactions = c.fetchall()
    return render_template('index.html', transactions=transactions)


@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        date = request.form['date']
        type_ = request.form['type']
        category = request.form['category']
        amount = float(request.form['amount'])
        description = request.form['description']

        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO transactions (date, type, category, amount, description) VALUES (?, ?, ?, ?, ?)",
                      (date, type_, category, amount, description))
            conn.commit()
        return redirect(url_for('index'))

    return render_template('add_transaction.html')


@app.route('/delete/<int:id>')
def delete_transaction(id):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM transactions WHERE id=?", (id,))
        conn.commit()
    return redirect(url_for('index'))


@app.route('/charts')
def charts():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Expense' GROUP BY category")
        data = c.fetchall()
    categories = [row[0] for row in data]
    totals = [row[1] for row in data]
    return render_template('charts.html', categories=categories, totals=totals)


@app.route('/export')
def export_csv():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM transactions")
        transactions = c.fetchall()

    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Date', 'Type', 'Category', 'Amount', 'Description'])
    cw.writerows(transactions)

    output = si.getvalue()
    return send_file(
        StringIO(output),
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"transactions_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    )


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
