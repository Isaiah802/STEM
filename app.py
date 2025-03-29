import sqlite3
import json
import serial  # You will need pyserial to read from the serial port
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import plotly.graph_objs as go
from datetime import datetime
import time

app = Flask(__name__)
socketio = SocketIO(app)

DATABASE = 'sensor_data.db'
SERIAL_PORT = 'COM3'  # Update this to match the serial port for your Arduino
BAUD_RATE = 9600

# Set up the serial connection to read data from Arduino
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Function to fetch the latest test results from the database
def get_latest_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = """
    SELECT TR.timestamp, TR.raw_data, S.sensor_type, T.test_type
    FROM TestResults TR
    JOIN Sensors S ON TR.sensor_id = S.sensor_id
    JOIN Tests T ON TR.test_id = T.test_id
    WHERE TR.timestamp > DATETIME('now', '-5 minutes')
    ORDER BY TR.timestamp DESC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    data = []
    for row in rows:
        timestamp = row[0]
        raw_data = json.loads(row[1])  # Assuming raw_data is stored as JSON
        sensor_type = row[2]
        test_type = row[3]
        
        data.append({
            'timestamp': timestamp,
            'sensor_type': sensor_type,
            'test_type': test_type,
            'raw_data': raw_data
        })

    conn.close()
    return data

# Function to generate plot for the graph
def generate_plot(data):
    timestamps = []
    sensor_data = []

    for entry in data:
        timestamps.append(entry['timestamp'])
        sensor_data.append(json.loads(entry['raw_data'])['value'])  # Extracting 'value' from the raw_data JSON

    # Plotly Graph
    trace = go.Scatter(
        x=timestamps,
        y=sensor_data,
        mode='lines+markers',
        name='Sensor Data'
    )

    layout = go.Layout(
        title='Real-time Sensor Data',
        xaxis=dict(title='Timestamp'),
        yaxis=dict(title='Sensor Value'),
    )

    fig = go.Figure(data=[trace], layout=layout)
    return fig.to_html(full_html=False)

# Socket event to push real-time data updates to the frontend
@socketio.on('get_real_time_data')
def handle_get_data():
    # Get latest data from database
    latest_data = get_latest_data()

    # Generate a plot based on latest data
    plot_html = generate_plot(latest_data)

    # Emit the plot to the frontend
    emit('update_graph', {'plot_html': plot_html})

# Background task for reading data from Arduino and inserting into database
def background_task():
    while True:
        # Read a line of data from the serial port
        if ser.in_waiting > 0:
            data_line = ser.readline().decode('utf-8').strip()  # Read and decode the line from Arduino
            sensor_values = data_line.split(',')  # Split the data into separate sensor values

            # Ensure there are exactly 4 sensor values (one for each sensor)
            if len(sensor_values) == 4:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Insert this data into the database for each sensor
                conn = sqlite3.connect(DATABASE)
                cursor = conn.cursor()

                for i, value in enumerate(sensor_values, start=1):  # Sensor IDs 1-4
                    raw_data = json.dumps({'value': int(value)})  # Store the sensor value in JSON format
                    
                    # Assuming test_id = 1 for simplicity, adjust if needed
                    cursor.execute("""
                    INSERT INTO TestResults (sensor_id, test_id, timestamp, raw_data)
                    VALUES (?, ?, ?, ?)
                    """, (i, 1, timestamp, raw_data))

                conn.commit()
                conn.close()

        # Wait for a short period (to avoid overloading the CPU)
        socketio.sleep(0.1)

# Start the background task to read data from Arduino
@socketio.on('connect')
def handle_connect():
    # Start background task when a user connects
    socketio.start_background_task(target=background_task)

if __name__ == '__main__':
    # Run the Flask app with SocketIO
    socketio.run(app, host='0.0.0.0', port=5000)
