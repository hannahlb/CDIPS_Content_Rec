import csv
import sqlite3
import sys

#
#The following lines increment the size limit for a csv field:
#https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072
#
maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True


#
# Convert Wikipedia.csv into Wikipedia.db, following Frank's tutorial
# http://www.datasciencebytes.com/bytes/2015/02/28/using-flask-to-answer-sql-queries/
#
csvfile="Wikipedia.csv"
dbfile="Wikipedia.db"

conn = sqlite3.connect(dbfile)
cur = conn.cursor()

cur.execute("""DROP TABLE IF EXISTS Wikipedia""")
cur.execute("""CREATE TABLE Wikipedia
            (id integer, website text, text_raw text)""")

with open(csvfile, 'r') as f:
    reader = csv.reader(f.readlines()[1:])  # exclude header line
    cur.executemany("""INSERT INTO Wikipedia VALUES (?,?,?)""",
                    (row for row in reader))
conn.commit()
conn.close()
