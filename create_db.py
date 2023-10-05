import sqlite3

conn = sqlite3.connect('expenses.db')
cur = conn.cursor()

cur.execute(""" CREATE TABLE IF NOT EXISTS  Expenses
(Id INTEGER PRIMARY KEY AUTOINCREMENT,
Date DATE,
Description TEXT,
Category TEXT,
price REAL)""")

conn.commit()
conn.close()
