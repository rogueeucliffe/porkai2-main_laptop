import serial
import time
import cv2
import numpy as np
import camera


# Open serial connection
ser = serial.Serial('COM4', 115200)  # Replace 'COM1' with the appropriate port
time.sleep(2)  # Allow some time for Arduino to initialize


# Given data
output_values = np.array([61, 55, 49, 43, 37, 31])
input_values = np.array(
    [
        [1, 203.3367599],
        [1, 198.6026289],
        [1, 177.917328],
        [1, 163.89361],
        [1, 152.4369501],
        [1, 138.5136842],
    ]
)

# Perform linear regression
coefficients = np.linalg.lstsq(input_values, output_values, rcond=None)[0]


# Define a function for calibration
def calibrate_input(input_value):
    # Apply linear transformation
    calibrated_output = np.dot(np.array([1, input_value]), coefficients)
    return calibrated_output


# Function to read sensor values
def read_sensor_values():
    sensor_values = []
    sensor_types = set()  # to keep track of collected sensor types
    while len(sensor_values) < 4:
        line = ser.readline().decode().strip()  # Read a line from serial and decode
        if (line.startswith("Temperature Sensor 1:") and "Temperature Sensor 1" not in sensor_types or
            line.startswith("pH value:") and "pH value" not in sensor_types or 
            line.startswith("Methane Concentration:") and "Methane Concentration" not in sensor_types or 
            line.startswith("Ammonia Concentration:") and "Ammonia Concentration" not in sensor_types):
            sensor_type, value = line.split(":")  # Extract the sensor type and value
            sensor_values.append(float(value.strip()))
            sensor_types.add(sensor_type.strip())
    # Get L* value
    camera.capture_image(1,'test.jpg')
    image = cv2.imread('test2.jpg')
    if image is None:
        print("Error loading image")
        return sensor_values
    
    L_star = get_L_star(image)
    
    # Append L* value to sensor data
    # calibrated_output = calibrate_input(L_star + 17)
    calibrated_output = calibrate_input(L_star)
    # print(f"Calibrated output for input {L_star}: {calibrated_output + 2}")
    # sensor_values.append(calibrated_output + 2)
    print(f"Calibrated output for input {L_star}: {calibrated_output}")
    sensor_values.append(calibrated_output)
    print(L_star)
    
    return sensor_values

def get_L_star(image):
    # converting the pork image to L*a*b* color space
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    # splitting L*a*b* channels
    L, a, b = cv2.split(lab_image)
    
    # calculating the average L* value
    L_mean = np.mean(L)

    L_mean = L_mean + 67
    
    return L_mean

# Main function
def main():
    # Capture an image
    
    # Read sensor values
    sensor_data = read_sensor_values()

    # Swap index 4 and 3
    sensor_data[3], sensor_data[4] = sensor_data[4], sensor_data[3]
    # Print sensor values as an array
    
    print("Sensor Values:", sensor_data)  

if __name__ == "__main__":
    main()
