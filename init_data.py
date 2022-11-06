import sqlite3

connection = sqlite3.connect('isoc.db')

cur = connection.cursor()

cur.executemany("INSERT INTO occupant_type (type_ID, type ) VALUES (?, ?)",
            [(1, 'OWNER'),(2,'TENANT')]
            )

cur.execute( "INSERT INTO society (name, address1, address2, city, pincode, reg_no, phone_no, email) \
                VALUES('Parijat Co-Op Housing Society','Dahanukar Colony , Lane No 5', 'Kothrud',\
                'Pune', '411038','SR101','9873293323','parijatchs@gmail.com') ")

connection.commit()
connection.close()
