import sqlite3

connection = sqlite3.connect('isoc.db')

cur = connection.cursor()

cur.executemany("INSERT INTO occupant_type (type_ID, type ) VALUES (?, ?)",
            [(1, 'OWNER'),(2,'TENANT')]
            )

connection.commit()
connection.close()
