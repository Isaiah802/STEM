import sqlite3

conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM TestResults LIMIT 10")
data = cursor.fetchall()

for row in data:
    print(row)

conn.close()
