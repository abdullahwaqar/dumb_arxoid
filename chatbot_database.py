import sqlite3

sql_transaction = []

connection = sqlite3.connect('data/db/data.db')

c = connection.cursor()