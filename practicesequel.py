import mysql.connector
from datetime import datetime

# create a connection to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Gu3ss1llTry1t0ut?",
    database="testdatabase"
)

mycursor = db.cursor()

# mycursor.execute("CREATE DATABASE testdatabase")

# Start writing queries
# mycursor.execute("CREATE TABLE Person (name VARCHAR(50), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)")
# mycursor.execute('DESCRIBE Person')
# for x in mycursor:
#   print(x)
# mycursor.execute("INSERT INTO Person (name, age) VALUES ('tim',45)")
# mycursor.execute("INSERT INTO Person (name, age) VALUES (%s,%s)", ("Joe", 22))
# db.commit()

# mycursor.execute("SELECT * FROM Person")

# mycursor.execute("CREATE TABLE Test (name varchar(50) NOT NULL, created datetime NOT NULL, gender ENUM('M','F', 'O') NOT NULL, id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")

# mycursor.execute("INSERT INTO Test (name, created, gender) VALUES(%s,%s,%s)", ("Joey", datetime.now(), 'F'))
# db.commit()

# mycursor.execute("SELECT id, name FROM Test WHERE gender = 'F' ORDER BY id DESC")

# mycursor.execute("ALTER TABLE Test ADD COLUMN food VARCHAR(50) NOT NULL")

# mycursor.execute("ALTER TABLE Test DROP food")

# mycursor.execute("ALTER TABLE Test CHANGE name first_name VARCHAR(50)")

# mycursor.execute("DESCRIBE Test")
# for x in mycursor:
    # print(x)

# FOREIGN KEYS!!!

users = [('tim', 'texhwithtim'),
         ('joe', 'joey123'),
         ('sarah', 'sarah1234')]

user_scores = [(45,100),
               (30,200),
               (46,124)]

# create parent table first
Q1 = "CREATE TABLE Users (id int PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50), passwd VARCHAR(50))"

# how to make the primary key the foreign key (for one-to-one table relationships)
Q2 = "CREATE TABLE Scores (userId int PRIMARY KEY, FOREIGN KEY(userId) REFERENCES Users(id), game1 int DEFAULT 0, game2 int DEFAULT 0)"

# mycursor.execute(Q1)
# mycursor.execute(Q2)

# mycursor.execute("SHOW TABLES")

# add list all at once

# mycursor.executemany("INSERT INTO Users (name, passwd) VALUES (%s, %s)", users)

Q3 = "INSERT INTO Users (name, passwd) VALUES (%s, %s)"
Q4 = "INSERT INTO Scores (userId, game1, game2) VALUES (%s, %s, %s)"

for x, user in enumerate(users):
    mycursor.execute(Q3, user)
    last_id = mycursor.lastrowid
    mycursor.execute(Q4, (last_id,) + user_scores[x])
db.commit()

mycursor.execute("SELECT * FROM Scores")
for x in mycursor:
    print(x)

mycursor.execute("SELECT * FROM Users")
for x in mycursor:
    print(x)