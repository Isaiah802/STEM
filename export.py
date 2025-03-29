import sqlite3
import csv

def export_to_csv(query, params, output_filename):
    # Connect to your SQLite database
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()

    # Execute the query with parameters
    cursor.execute(query, params)
    
    # Open a CSV file to write the results
    with open(output_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow([description[0] for description in cursor.description])

        # Write the data
        for row in cursor.fetchall():
            writer.writerow(row)

    # Close the connection
    conn.close()

# Example query to get all test results for a specific bridge and test type
query = """
SELECT TR.*, S.sensor_type, T.test_type
FROM TestResults TR
JOIN Sensors S ON TR.sensor_id = S.sensor_id
JOIN Tests T ON TR.test_id = T.test_id
WHERE S.bridge = ? AND T.test_type = ?;
"""

params = ('Bridge 1', 'Vibration')  # Replace with your bridge name and test type
export_to_csv(query, params, 'bridge_1_vibration_test_results.csv')

# export_to_csv(query, ('Bridge 1', 'Weight'), 'bridge_1_weight_test_results.csv')
# export_to_csv(query, ('Bridge 2', 'Vibration'), 'bridge_2_vibration_test_results.csv')
