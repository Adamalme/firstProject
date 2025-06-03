import sqlite3

conn = sqlite3.connect('transactions.db')
c = conn.cursor()

# Create the transactions table
c.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        type TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT
    )
''')

conn.commit()
conn.close()

print("Database initialized and table created successfully.")
