import sqlite3

connection = sqlite3.connect('isoc.db')

cur = connection.cursor()

cur.executemany("INSERT INTO person_type (type_ID, type ) VALUES (?, ?)",
            [(1, 'OWNER'),(2,'TENANT'),(3,'VISITOR')]
            )

connection.commit()
connection.close()
