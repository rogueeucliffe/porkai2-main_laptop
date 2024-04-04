import serial
import time

# Open serial connection
ser = serial.Serial('COM8', 115200)  # Replace 'COM1' with the appropriate port
time.sleep(2)  # Allow some time for Arduino to initialize

# Function to read sensor values
def read_sensor_values():
    sensor_values = []
    while len(sensor_values) < 4:
        line = ser.readline().decode().strip()  # Read a line from serial and decode
        if line.startswith("temp 1:") or line.startswith("pH Value:") or line.startswith("Methane Concentration:") or line.startswith("Ammonia Concentration:"):
            value = float(line.split(":")[1].strip())  # Extract the sensor value
            sensor_values.append(value)
    return sensor_values

# Main function
def main():
    while True:
        sensor_data = read_sensor_values()
        print("Sensor Values:", sensor_data)  # Print sensor values as an array

if __name__ == "__main__":
    main()
