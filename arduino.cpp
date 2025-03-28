// Define the pin numbers for each sensor's signal pin
const int sensor1Pin = A0; // Sensor 1 connected to analog pin A0
const int sensor2Pin = A1; // Sensor 2 connected to analog pin A1
const int sensor3Pin = A2; // Sensor 3 connected to analog pin A2
const int sensor4Pin = A3; // Sensor 4 connected to analog pin A3

void setup() {
  // Start serial communication at 9600 baud rate
  Serial.begin(9600);
}

void loop() {
  // Read the analog values from each sensor
  int sensor1Value = analogRead(sensor1Pin); // Read the value from sensor 1
  int sensor2Value = analogRead(sensor2Pin); // Read the value from sensor 2
  int sensor3Value = analogRead(sensor3Pin); // Read the value from sensor 3
  int sensor4Value = analogRead(sensor4Pin); // Read the value from sensor 4

  // Send the sensor values over the serial port in a comma-separated format
  Serial.print(sensor1Value);  // Send Sensor 1 data
  Serial.print(",");
  Serial.print(sensor2Value);  // Send Sensor 2 data
  Serial.print(",");
  Serial.print(sensor3Value);  // Send Sensor 3 data
  Serial.print(",");
  Serial.println(sensor4Value); // Send Sensor 4 data
  
  // Wait for a short period (adjust as needed) before sending the next set of data
  delay(100); // Delay in milliseconds (100ms = 10 readings per second)
}
