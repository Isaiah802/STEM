import sqlite3

# Connect to the database
conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()

# List of tables to delete data from
tables = ['Sensors', 'Tests', 'TestResults', 'CleanedData', 'Analysis']

# Check if each table exists before deleting data
for table in tables:
    try:
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        if cursor.fetchone():
            cursor.execute(f"DELETE FROM {table}")
            print(f"All data deleted from {table}")
        else:
            print(f"Table {table} does not exist.")
    except sqlite3.Error as e:
        print(f"Error deleting data from {table}: {e}")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data deletion process completed.")
