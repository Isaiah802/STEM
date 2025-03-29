import sqlite3 
import random
import json
from datetime import datetime, timedelta

# Function to generate random sensor data (a single voltage value)
def generate_random_voltage():
    return random.uniform(0, 5)  # Assuming the sensor generates a voltage between 0 and 5V

# Function to generate a timestamp that increments by one second for each value
def generate_incrementing_timestamp(base_time):
    """Increment the timestamp by 1 second each time."""
    new_timestamp = base_time + timedelta(seconds=1)
    return new_timestamp.strftime('%Y-%m-%d %H:%M:%S')  # Format: Y-M-D Hour:Min:Sec

try:
    # Connect to the database
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()

    # Enable foreign key support
    cursor.execute('PRAGMA foreign_keys = ON')

    # Insert data for sensor 4 (auto-incremented sensor_id)
    sensor_type = 'Piezoelectric'
    bridge = f'Bridge {random.choice([1, 2])}'
    position = random.choice(['A', 'B', 'C', 'D'])
    status = 'active'
    serial_number = f'SN00005'  # Serial number for sensor 4: SN00004

    cursor.execute(''' 
    INSERT INTO Sensors (sensor_type, bridge, position, status, serial_number)
    VALUES (?, ?, ?, ?, ?)
    ''', (sensor_type, bridge, position, status, serial_number))

    # Insert test data for test 5
    test_id = 5  # Set the test ID to 5
    test_type = 'Weight'  # Example test type
    description = f'Description for {test_type} test'
    cursor.execute('''
    INSERT INTO Tests (test_id, test_type, description)
    VALUES (?, ?, ?)
    ''', (test_id, test_type, description))

    # Start with a base timestamp for the test data
    base_time = datetime.now()

    # Insert sample data into TestResults and CleanedData for sensor 4, test 5
    for i in range(20):  # Generate 20 entries for test 5 and sensor 4
        # Insert data into TestResults table
        timestamp = generate_incrementing_timestamp(base_time)  # Generate incrementing timestamp
        raw_voltage = generate_random_voltage()  # Generate random voltage reading for sensor 4
        
        # Store raw data as a JSON object
        raw_data = json.dumps({"voltage": raw_voltage})
        
        cursor.execute('''
        INSERT INTO TestResults (sensor_id, test_id, timestamp, raw_data)
        VALUES ((SELECT sensor_id FROM Sensors WHERE serial_number = 'SN00005'), ?, ?, ?)
        ''', (test_id, timestamp, raw_data))

        # Fetch the result_id for the newly inserted test result
        cursor.execute('''
        SELECT last_insert_rowid()
        ''')
        result_id = cursor.fetchone()[0]  # Get the last inserted result_id

        # Insert cleaned data into CleanedData table
        cleaned_data = raw_voltage * random.uniform(0.95, 1.05)  # Slightly modify raw data for cleaned data
        cleaned_by = f'User{4}'  # Simulate cleanup by user based on sensor_id
        
        # Store cleaned data as a JSON object
        cleaned_data_json = json.dumps({"voltage": cleaned_data})

        cursor.execute('''
        INSERT INTO CleanedData (result_id, cleaned_data, cleaned_by)
        VALUES (?, ?, ?)
        ''', (result_id, cleaned_data_json, cleaned_by))  # Store cleaned data

        # Increment base time by 1 second for the next entry
        base_time += timedelta(seconds=1)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Database populated with sample records for Sensor 4 and Test 5.")

except sqlite3.Error as e:
    print(f"SQLite error: {e}")
except Exception as e:
    print(f"Error: {e}")
