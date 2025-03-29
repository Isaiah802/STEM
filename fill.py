import sqlite3
import random
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
    # Connect to the database (create it if it doesn't exist)
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()

    # Enable foreign key support (in case foreign key constraints are turned off by default)
    cursor.execute('PRAGMA foreign_keys = ON')

    # Clear existing records (optional, based on your needs)
    cursor.execute('DELETE FROM CleanedData')
    cursor.execute('DELETE FROM TestResults')
    cursor.execute('DELETE FROM Tests')
    cursor.execute('DELETE FROM Sensors')

    # Insert sample data into Sensors table (4 sensors with specific IDs)
    sensor_ids = [1, 2, 3, 4]  # Sensor IDs are fixed to 1, 2, 3, and 4
    for sensor_id in sensor_ids:  # Only insert 4 sensors
        sensor_type = 'Piezoelectric'
        bridge = f'Bridge {random.choice([1, 2])}'
        position = random.choice(['A', 'B', 'C', 'D'])
        status = 'active'
        serial_number = f'SN{sensor_id:05}'  # Serial number from SN00001 to SN00004

        cursor.execute('''
        INSERT INTO Sensors (sensor_id, sensor_type, bridge, position, status, serial_number)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (sensor_id, sensor_type, bridge, position, status, serial_number))

    # Insert a single test data entry into the Tests table (test_id = 1)
    test_id = 1  # Set the test ID to 1
    test_type = 'Weight'  # Only one test type, for example, 'Weight'
    description = f'Description for {test_type} test'
    cursor.execute('''
    INSERT INTO Tests (test_id, test_type, description)
    VALUES (?, ?, ?)
    ''', (test_id, test_type, description))

    # Start with a base timestamp
    base_time = datetime.now()

    # Insert sample data into TestResults table (20 values for each sensor, for test_id = 1)
    # Insert sample data into CleanedData table (20 values per sensor)
    for sensor_id in sensor_ids:  # Loop over each of the 4 sensors
        for i in range(20):  # Generate 20 cleaned data values for each sensor
            # Fetch the correct result_id for the current sensor and test_id
            cursor.execute('''
            SELECT result_id FROM TestResults
            WHERE sensor_id = ? AND test_id = ? ORDER BY timestamp LIMIT 1
            ''', (sensor_id, test_id))
            result_id = cursor.fetchone()[0]  # Get the result_id for the current sensor

            # Cleaned data would be a slightly modified version of raw data (for demonstration purposes)
            cleaned_data = generate_random_voltage()  # Cleaned data (random voltage value again)

            cleaned_by = f'User{sensor_id}'  # Simulating user cleanup by sensor ID
            
            cursor.execute('''
            INSERT INTO CleanedData (result_id, cleaned_data, cleaned_by)
            VALUES (?, ?, ?)
            ''', (result_id, cleaned_data, cleaned_by))  # Store cleaned_data as REAL (no need for json.dumps)

    # Insert sample data into CleanedData table (20 values per sensor)
    for sensor_id in sensor_ids:  # Loop over each of the 4 sensors
        for i in range(20):  # Generate 20 cleaned data values for each sensor
            # Get the result_id from the TestResults table (using result_id from the previous insert)
            cursor.execute('SELECT last_insert_rowid()')
            result_id = cursor.fetchone()[0]  # Get the last inserted result_id

            # Cleaned data would be a slightly modified version of raw data (for demonstration purposes)
            cleaned_data = generate_random_voltage()  # Cleaned data (random voltage value again)

            cleaned_by = f'User{sensor_id}'  # Simulating user cleanup by sensor ID
            
            cursor.execute('''
            INSERT INTO CleanedData (result_id, cleaned_data, cleaned_by)
            VALUES (?, ?, ?)
            ''', (result_id, cleaned_data, cleaned_by))  # Store cleaned_data as REAL (no need for json.dumps)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Database populated with sample records.")

except sqlite3.Error as e:
    print(f"SQLite error: {e}")
except Exception as e:
    print(f"Error: {e}")
