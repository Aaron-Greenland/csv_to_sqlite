# Convert csv to sqlite

import csv
import sqlite3
import os

filename = input('Enter the name of the csv file: ')
filename_sqlite = filename.split('.')[0] + '.db'


# Create a new database
conn = sqlite3.connect(filename_sqlite)
c = conn.cursor()

# Create a new table
c.execute('''CREATE TABLE data
                (id INTEGER PRIMARY KEY, time INTEGER, data INTEGER
                )''')

# Read data from csv
with open(filename, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        c.execute('INSERT INTO data (time, data) VALUES (?, ?)', (row[0], row[1]))

# Save (commit) the changes
conn.commit()
conn.close()

