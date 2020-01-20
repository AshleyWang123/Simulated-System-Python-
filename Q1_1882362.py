import sqlite3
import random, string, math

# Create table Tasks
db=sqlite3.connect("Dataset.db")
cursor=db.cursor()
cursor.execute( "CREATE TABLE Tasks ("
    "ID TEXT PRIMARY KEY NOT NULL,"
    "Arrival FLOAT NOT NULL,"
    "Duration INTERGER NOT NULL)")

# Insert data
for i in range(100):
    # be randomly chosen (uniform probability).
    ID=''.join(random.sample(string.ascii_letters+string.digits+'@_#*-&',6))

    Arrival= random.uniform(0,100) #uniform distribution.

    Duration=math.ceil(random.expovariate(1))#exponential distribution; rounded up.

    cursor.execute("INSERT INTO tasks VALUES (?,?,?)", (ID,Arrival,Duration))

db.commit()
cursor.close()
