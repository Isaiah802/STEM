import sqlite3
import json

def print_sensors():
    print("Sensors Table:")
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Sensors")
    sensors = cursor.fetchall()

    if not sensors:
        print("No data in Sensors table.")
    else:
        for sensor in sensors:
            print(f"Sensor ID: {sensor[0]}, Type: {sensor[1]}, Bridge: {sensor[2]}, Position: {sensor[3]}, Status: {sensor[4]}, Serial Number: {sensor[5]}")

    conn.close()
    print("\n")

def print_tests():
    print("Tests Table:")
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Tests")
    tests = cursor.fetchall()

    if not tests:
        print("No data in Tests table.")
    else:
        for test in tests:
            print(f"Test ID: {test[0]}, Type: {test[1]}, Description: {test[2]}, Units: {test[3]}")

    conn.close()
    print("\n")

def print_test_results():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM TestResults")
    test_results = cursor.fetchall()

    if not test_results:
        print("No data in TestResults table.")
    else:
        for result in test_results:
            result_id = result[0]
            sensor_id = result[1]
            test_id = result[2]
            timestamp = result[3]
            raw_data = result[4]

            # Check if raw_data is stored as a JSON string (in case it's a float, we'll just print it)
            try:
                # Attempt to parse raw_data as JSON (for future-proofing)
                raw_data = float(raw_data)
            except ValueError:
                pass  # If it's already a float, do nothing

            print(f"Result ID: {result_id}, Sensor ID: {sensor_id}, Test ID: {test_id}, Timestamp: {timestamp}, Raw Data: {raw_data}")

    conn.close()
    print("\n")

def print_cleaned_data():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM CleanedData")
    cleaned_data = cursor.fetchall()

    if not cleaned_data:
        print("No data in CleanedData table.")
    else:
        for data in cleaned_data:
            cleaned_data_id = data[0]
            result_id = data[1]
            cleaned_data_value = data[2]
            cleaned_by = data[3]
            cleaned_at = data[4]

            # Check if cleaned_data_value is stored as a float (if so, print it directly)
            try:
                # Try casting cleaned_data_value to a float (if it's not a string)
                cleaned_data_value = float(cleaned_data_value)
            except ValueError:
                pass  # If it's already a float, do nothing

            print(f"Cleaned Data ID: {cleaned_data_id}, Result ID: {result_id}, Cleaned Data: {cleaned_data_value}, Cleaned By: {cleaned_by}, Cleaned At: {cleaned_at}")

    conn.close()
    print("\n")

def print_all_data():
    print_sensors()
    print_tests()
    print_test_results()
    print_cleaned_data()

if __name__ == '__main__':
    print_all_data()
