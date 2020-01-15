import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE users (id INTEGER PRIMARY KEY,username text,password text)"
cursor.execute(create_table)

item_table = "CREATE TABLE items (name text,price real)"
cursor.execute(item_table)


connection.commit()
connection.close()
