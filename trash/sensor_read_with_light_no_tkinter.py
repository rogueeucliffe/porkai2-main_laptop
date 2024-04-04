import serial
import time
import cv2
import numpy as np

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

def get_L_star(image):
    # converting the pork image to L*a*b* color space
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    # splitting L*a*b* channels
    L, a, b = cv2.split(lab_image)
    
    # calculating the average L* value
    L_mean = np.mean(L)
    
    return L_mean

# Main function
def main():
    # Load the image
    try:
        image = cv2.imread('test.jpg')
        if image is None:
            raise FileNotFoundError("Image file not found or could not be opened.")
    except Exception as e:
        print("Error loading image:", e)
        return
    
    # Get L* value
    L_star = get_L_star(image)

    # Read sensor values
    sensor_data = read_sensor_values()
    
    # Append L* value to sensor data
    sensor_data.append(L_star)
    
    # Print sensor values as an array
    print("Sensor Values:", sensor_data)  

if __name__ == "__main__":
    main()
