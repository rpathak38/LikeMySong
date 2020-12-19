import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="music123",
    database="musicdb"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM music_data")

myresult = mycursor.fetchall()

for row in myresult:
    print(row)
