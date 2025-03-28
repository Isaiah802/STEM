import os
import sqlite3
import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import plotly.graph_objs as go
import pandas as pd
import random
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

DATABASE = 'sensor_data.db'

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
        sensor_data.append(entry['raw_data'])  # Assuming raw_data contains the actual values to plot

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

# Background task for simulating real-time data updates
def background_task():
    while True:
        # Simulate new data arrival by generating random data (for testing purposes)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        raw_data = random.randint(10, 100)  # Example raw data
        
        # Save this simulated data to the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO TestResults (sensor_id, test_id, timestamp, raw_data)
        VALUES (?, ?, ?, ?)
        """, (1, 1, timestamp, json.dumps({'value': raw_data})))  # Example sensor_id=1, test_id=1
        
        conn.commit()
        conn.close()

        socketio.sleep(5)  # Sleep for 5 seconds before generating the next data

# Start the background task to simulate data
@socketio.on('connect')
def handle_connect():
    # Start background task when a user connects
    socketio.start_background_task(target=background_task)

if __name__ == '__main__':
    # Run the Flask app with SocketIO
    socketio.run(app, host='0.0.0.0', port=5000)
