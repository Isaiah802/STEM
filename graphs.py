import matplotlib.pyplot as plt
import sqlite3
import argparse
from datetime import datetime

# Function to plot a time-series graph (Voltage over time)
def plot_time_series(sensor_id, test_id):
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()

    # Adjust query to fetch data in chronological order
    cursor.execute("""
    SELECT timestamp, raw_data FROM TestResults
    WHERE sensor_id = ? AND test_id = ?
    ORDER BY timestamp
    """, (sensor_id, test_id))
    data = cursor.fetchall()

    if not data:
        print(f"No data found for Sensor ID: {sensor_id} and Test ID: {test_id}")
        return

    # Debugging: print fetched data
    print(f"Fetched data for sensor {sensor_id}, test {test_id}: {data}")

    # Extract timestamps and raw_data (raw_data is already a float)
    timestamps = [entry[0] for entry in data]
    raw_data = [entry[1] for entry in data]

    # Convert timestamps to datetime objects for proper plotting
    timestamps = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in timestamps]

    # Plot the time-series graph
    plt.plot(timestamps, raw_data, label=f'Sensor {sensor_id} Test {test_id}')
    plt.xlabel('Time')
    plt.ylabel('Voltage (Raw Data)')
    plt.title('Voltage Over Time for Test')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    # Save the plot as a PNG file with a timestamp
    plt.savefig(f'time_series_sensor_{sensor_id}_test_{test_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')

    # Show the plot
    plt.show()

    conn.close()

# Function to plot a scatter plot between two sensors
def plot_scatter(sensor_id1, test_id1, sensor_id2, test_id2):
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()

    # Fetch data for sensor 1 with timestamps
    cursor.execute("""
    SELECT timestamp, raw_data FROM TestResults WHERE sensor_id = ? AND test_id = ?
    """, (sensor_id1, test_id1))
    data1 = cursor.fetchall()

    # Fetch data for sensor 2 with timestamps
    cursor.execute("""
    SELECT timestamp, raw_data FROM TestResults WHERE sensor_id = ? AND test_id = ?
    """, (sensor_id2, test_id2))
    data2 = cursor.fetchall()

    if not data1 or not data2:
        print("No data found for one or both sensors.")
        return

    # Convert data to dictionaries based on timestamp for easy matching
    data1_dict = {entry[0]: entry[1] for entry in data1}
    data2_dict = {entry[0]: entry[1] for entry in data2}

    # Find common timestamps for both sensors
    common_timestamps = set(data1_dict.keys()).intersection(data2_dict.keys())

    if not common_timestamps:
        print("No common timestamps found between the two sensors.")
        return

    # Extract matching data points based on common timestamps
    raw_data1 = [data1_dict[ts] for ts in common_timestamps]
    raw_data2 = [data2_dict[ts] for ts in common_timestamps]

    # Plot the scatter graph
    plt.scatter(raw_data1, raw_data2, label=f'Sensor {sensor_id1} vs Sensor {sensor_id2}')
    plt.xlabel(f'Sensor {sensor_id1} Raw Data')
    plt.ylabel(f'Sensor {sensor_id2} Raw Data')
    plt.title(f'Scatter Plot between Sensor {sensor_id1} and Sensor {sensor_id2}')
    plt.legend()
    plt.tight_layout()

    # Save the plot as a PNG file
    plt.savefig(f'scatter_sensor_{sensor_id1}_{sensor_id2}_test_{test_id1}_{test_id2}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')

    # Show the plot
    plt.show()

    conn.close()

# Function to plot a histogram
def plot_histogram(sensor_id, test_id):
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT raw_data FROM TestResults WHERE sensor_id = ? AND test_id = ?
    """, (sensor_id, test_id))
    data = cursor.fetchall()

    if not data:
        print(f"No data found for Sensor ID: {sensor_id} and Test ID: {test_id}")
        return

    # raw_data is already a float
    raw_data = [entry[0] for entry in data]

    plt.hist(raw_data, bins=20, color='blue', edgecolor='black')
    plt.title(f"Histogram of Sensor {sensor_id} Test {test_id} Raw Data")
    plt.xlabel('Voltage')
    plt.ylabel('Frequency')
    plt.tight_layout()

    # Save the plot as a PNG file
    plt.savefig(f'histogram_sensor_{sensor_id}_test_{test_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')

    # Show the plot
    plt.show()

    conn.close()

# Function to plot a boxplot
def plot_boxplot(sensor_id, test_id):
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT raw_data FROM TestResults WHERE sensor_id = ? AND test_id = ?
    """, (sensor_id, test_id))
    data = cursor.fetchall()

    if not data:
        print(f"No data found for Sensor ID: {sensor_id} and Test ID: {test_id}")
        return

    # raw_data is already a float
    raw_data = [entry[0] for entry in data]

    # Plot the boxplot
    plt.boxplot(raw_data)
    plt.title(f"Boxplot of Sensor {sensor_id} Test {test_id} Raw Data")
    plt.ylabel('Voltage')
    plt.tight_layout()

    # Save the plot as a PNG file
    plt.savefig(f'boxplot_sensor_{sensor_id}_test_{test_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')

    # Show the plot
    plt.show()

    conn.close()

# Main function to handle the command-line interface
def main():
    parser = argparse.ArgumentParser(description='Visualize sensor data.')
    parser.add_argument('graph', choices=['time_series', 'scatter', 'histogram', 'boxplot'], 
                        help='The type of graph to generate.')
    parser.add_argument('--sensor_id1', type=int, help='Sensor ID for the first sensor (required for scatter).')
    parser.add_argument('--sensor_id2', type=int, help='Sensor ID for the second sensor (required for scatter).')
    parser.add_argument('--test_id1', type=int, help='Test ID for the first test (required for scatter and time_series).')
    parser.add_argument('--test_id2', type=int, help='Test ID for the second test (required for scatter).')

    args = parser.parse_args()

    if args.graph == 'time_series':
        sensor_id = int(input('Enter Sensor ID: '))
        test_id = int(input('Enter Test ID: '))
        plot_time_series(sensor_id, test_id)
    elif args.graph == 'scatter':
        if not args.sensor_id1 or not args.sensor_id2 or not args.test_id1 or not args.test_id2:
            print("Please provide both sensor IDs and test IDs for scatter plot.")
        else:
            plot_scatter(args.sensor_id1, args.test_id1, args.sensor_id2, args.test_id2)
    elif args.graph == 'histogram':
        sensor_id = int(input('Enter Sensor ID: '))
        test_id = int(input('Enter Test ID: '))
        plot_histogram(sensor_id, test_id)
    elif args.graph == 'boxplot':
        sensor_id = int(input('Enter Sensor ID: '))
        test_id = int(input('Enter Test ID: '))
        plot_boxplot(sensor_id, test_id)

if __name__ == '__main__':
    main()


# python graphs.py time_series

# python graphs.py histogram

# python graphs.py scatter --sensor_id1 1 --sensor_id2 2 --test_id1 1 --test_id2 2
# python graphs.py scatter --sensor_id1 <sensor_id_1> --test_id1 <test_id_1> --sensor_id2 <sensor_id_2> --test_id2 <test_id_2>

# python graphs.py boxplot

#python graphs.py bar_chart


#python graphs.py time_series
#python graphs.py scatter --sensor_id1 1 --sensor_id2 2 --test_id1 1 --test_id2 2
#python graphs.py boxplot
