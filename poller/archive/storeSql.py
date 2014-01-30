import MySQLdb

db = MySQLdb.connect(host="localhost", port=3306,
    user="crawler", passwd="disaggreg8tor",
    db="firsttest");
cursor = db.cursor()

x = 1
mainString = "INSERT INTO energydata (timestamp, power) VALUES (%s, %s)"
while x < 10:
    print(x)
    data = (x,x)
    insertString = mainString % data
    try:
        cursor.execute(insertString)
        db.commit()
    except:
        db.rollback()
    x += 1
db.close
