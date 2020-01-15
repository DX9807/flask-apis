import sqlite3


connection = sqlite3.connect('data.db')
cursor = connection.cursor()


create_table = "CREATE TABLE users (id int,username text,password text)"

cursor.execute(create_table)

user = (
       (1,'bob','asdf'),
       (2,'Jose','asdf'),
       (3,'Jhon','zxcv')
       )

insert_query = "INSERT INTO users VALUES(?,?,?)"
cursor.executemany(insert_query,user)

select_query = "SELECT *FROM users"
result = cursor.execute(select_query)
print(result.fetchall())


select_one = "SELECT * FROM users WHERE username=?"
res=cursor.execute(select_one,('bob',))
print(res)
print(res.fetchone())

connection.commit()
connection.close()
