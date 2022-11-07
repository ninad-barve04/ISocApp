import sqlite3 as sql

conn = sql.connect("isoc.db")

conn_cursor = conn.cursor()

conn_cursor.execute("DROP TABLE IF EXISTS society")
conn_cursor.execute("DROP TABLE IF EXISTS person_type")
conn_cursor.execute("DROP TABLE IF EXISTS occupant_type")
conn_cursor.execute("DROP TABLE IF EXISTS person")
conn_cursor.execute("DROP TABLE IF EXISTS vehicle_type")
conn_cursor.execute("DROP TABLE IF EXISTS vehicle")
conn_cursor.execute("DROP TABLE IF EXISTS visitor_entry")
conn_cursor.execute("DROP TABLE IF EXISTS flat")
conn_cursor.execute("DROP TABLE IF EXISTS occupies")
conn_cursor.execute("DROP TABLE IF EXISTS flat_owner_history_table")
conn_cursor.execute("DROP TABLE IF EXISTS flat_owner_file_record_table")
conn_cursor.execute("DROP TABLE IF EXISTS flat_occupant_history_table")
conn_cursor.execute("DROP TABLE IF EXISTS occupant_type")
conn_cursor.execute("DROP TABLE IF EXISTS maintainance")


society_table = """
CREATE TABLE society (
    type_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(256),
    address1 VARCHAR(256),
    address2 VARCHAR(256),
    city VARCHAR(32),
    pincode VARCHAR(12),
    reg_no  VARCHAR(96),
    phone_no VARCHR(24),
    email   VARCHAR(64)
);
"""
#    CONSTRAINT society_pk PRIMARY KEY (type_ID)


occupant_type_table = """
CREATE TABLE occupant_type (
    type_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    type VARCHAR(16)
);
"""

person_table = """
CREATE TABLE person (
    person_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(256),
    phone_number CHAR(10)
);
"""

vehicle_type_table = """
CREATE TABLE vehicle_type (
    type_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    type VARCHAR(16)
);
"""

vehicle_table = """
CREATE TABLE vehicle (
    vehicle_ID VARCHAR(16) PRIMARY KEY NOT NULL,
    make VARCHAR(32),
    model VARCHAR(32),
    owner_ID INTEGER,
    type INTEGER,
    CONSTRAINT vehicle_fk1 FOREIGN KEY (owner_ID) REFERENCES person(person_ID),
    CONSTRAINT vehicle_fk2 FOREIGN KEY (type) REFERENCES vehicle_type(type_ID)
);
"""

flat_table = """
CREATE TABLE flat (
    flat_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    flat_no VARCHAR(8),
    bldg_no VARCHAR(8),
    floor_no INTEGER,
    area DOUBLE,
    occupant_ID INTEGER,
    CONSTRAINT flat_fk1 FOREIGN KEY (occupant_ID) REFERENCES person(person_ID),
    CONSTRAINT flat_uniq_id UNIQUE (flat_no,bldg_no,floor_no)
);
"""

visitor_entry_table = """
CREATE TABLE visitor_entry (
    entry_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    visitor_ID INTEGER,
    flat_ID INTEGER,
    visitee_ID INTEGER,
    entry_time VARCHAR(24),
    exit_time VARCHAR(24),
    vehicle_number VARCHAR(16),
    no_of_people INTEGER,
    CONSTRAINT `visitor_entry_fk1` FOREIGN KEY (visitor_ID) REFERENCES person(person_ID),
    CONSTRAINT `visitor_entry_fk2` FOREIGN KEY (flat_ID) REFERENCES flat(flat_ID),
    CONSTRAINT `visitor_entry_fk3` FOREIGN KEY (visitee_ID) REFERENCES person(person_ID)
);
"""

# occupant_table = """
# CREATE TABLE occupies (
#     occupant_ID INTEGER PRIMARY KEY NOT NULL,
#     flat_ID INTEGER,
#     CONSTRAINT `occupant_fk1` FOREIGN KEY (occupant_ID) REFERENCES person(person_ID),
#     CONSTRAINT `occupant_fk2` FOREIGN KEY (flat_ID) REFERENCES flat(flat_ID)
# );
# """

owner_history_table = """
CREATE TABLE flat_owner_history_table (
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    flat_ID INTEGER NOT NULL,
    person_ID INTEGER NOT NULL,
    purchase_date VARCHAR(24),
    sale_date VARCHAR(24),
    CONSTRAINT owner_history_fk1 FOREIGN KEY (flat_ID) REFERENCES flat(flat_ID),
    CONSTRAINT owner_history_fk2 FOREIGN KEY (person_ID) REFERENCES person(person_ID),
    CONSTRAINT owner_history_unique_id UNIQUE (flat_ID, person_ID, purchase_date, sale_date)
);
"""


owner_file_record_table = """
CREATE TABLE flat_owner_file_record_table (
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    history_ID INTEGER,
    filepath VARCHAR(128),
    CONSTRAINT owner_file_fk1 FOREIGN KEY (history_ID) REFERENCES flat_owner_history_table(ID)
);
"""


occupant_history_table = """
CREATE TABLE flat_occupant_history_table (
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    flat_ID INTEGER NOT NULL,
    person_ID INTEGER NOT NULL,
    type INTEGER NOT NULL,
    from_date VARCHAR(24),
    end_date VARCHAR(24),
    CONSTRAINT tenant_history_fk1 FOREIGN KEY (flat_ID) REFERENCES flat(flat_ID),
    CONSTRAINT tenant_history_fk2 FOREIGN KEY (person_ID) REFERENCES person(person_ID),
    CONSTRAINT tenant_history_fk3 FOREIGN KEY (type) REFERENCES occupant_type(type_ID),
    CONSTRAINT occupant_history_unique_id UNIQUE (flat_ID, person_ID, type, from_date, end_date)
);
"""


maintainance = """
CREATE TABLE maintainance (
    maintainance_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    period VARCHAR(16),
    payment_date VARCHAR(10),
    payment_method VARCHAR(16),
    amt_paid INTEGER,
    amt_due INTEGER,
    flat_ID INTEGER,
    FOREIGN KEY (flat_ID) REFERENCES flat(flat_ID)
);
"""


conn_cursor.execute(society_table)
conn_cursor.execute(occupant_type_table)
conn_cursor.execute(person_table)
conn_cursor.execute(vehicle_type_table)
conn_cursor.execute(vehicle_table)
conn_cursor.execute(visitor_entry_table)
conn_cursor.execute(flat_table)
conn_cursor.execute(owner_history_table)
conn_cursor.execute(occupant_history_table)
# conn_cursor.execute(occupant_table)
conn_cursor.execute(maintainance)
conn_cursor.execute(owner_file_record_table)

conn.commit()
conn.close()
