import sqlite3

# Connect to (or create) a new SQLite database file
conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()

# Create tables with your updated schema

cursor.execute('''
CREATE TABLE IF NOT EXISTS Sensors (
    sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_type TEXT NOT NULL DEFAULT 'Piezoelectric',
    bridge TEXT NOT NULL,  -- Bridge 1 or Bridge 2
    position TEXT NOT NULL,  -- Position A, B, C, D
    status TEXT DEFAULT 'active',  -- active, inactive, etc.
    serial_number TEXT UNIQUE
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Tests (
    test_id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_type TEXT NOT NULL,  -- e.g., "Weight", "Vibration", "Break"
    description TEXT,
    units TEXT DEFAULT 'N/A'  -- Units of measurement
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS TestResults (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER,
    test_id INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    raw_data JSON,
    FOREIGN KEY (sensor_id) REFERENCES Sensors(sensor_id),
    FOREIGN KEY (test_id) REFERENCES Tests(test_id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS CleanedData (
    cleaned_data_id INTEGER PRIMARY KEY AUTOINCREMENT,
    result_id INTEGER,
    cleaned_data JSON,
    cleaned_by TEXT,  -- Who cleaned the data
    cleaned_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- When was it cleaned
    FOREIGN KEY (result_id) REFERENCES TestResults(result_id)
);
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database schema created successfully!")
