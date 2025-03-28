import sqlite3

def check_data_exists(sensor_id, test_id):
    # Connect to the database
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()

    # Query to check if there is any data for the given sensor_id and test_id
    cursor.execute("""
    SELECT COUNT(*) FROM TestResults WHERE sensor_id = ? AND test_id = ?
    """, (sensor_id, test_id))

    # Fetch the result
    result = cursor.fetchone()

    # If result[0] is greater than 0, it means data exists
    if result[0] > 0:
        print(f"Data exists for Sensor ID {sensor_id} and Test ID {test_id}")
    else:
        print(f"No data found for Sensor ID {sensor_id} and Test ID {test_id}")

    # Close the connection
    conn.close()

# Example usage:
sensor_id = int(input('Enter Sensor ID: '))
test_id = int(input('Enter Test ID: '))
check_data_exists(sensor_id, test_id)
