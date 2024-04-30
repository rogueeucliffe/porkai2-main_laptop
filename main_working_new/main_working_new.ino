#include <DHT.h>

#define DHTTYPE DHT11

// Pin assignments for DHT sensors.
const int DHT_PIN_1 = 2; // Connect the first sensor to digital pin 2.
const int DHT_PIN_2 = 3; // Connect the second sensor to digital pin 3.

// Create instances of the DHT class for each sensor.
DHT dht1(DHT_PIN_1, DHTTYPE);
DHT dht2(DHT_PIN_2, DHTTYPE);


const int AO_Pin = A0;
const int A1_Pin = A1;
const int A2_Pin = A2; // New pin for pH sensor
int AO_Out; // Declare variable to store AO pin reading
int A1_Out; // Declare variable to store A1 pin reading
int A2_Out; // Declare variable to store A2 pin reading

// Calibration parameters
float AO_Slope = 1; // Calibration slope for AO pin
int AO_Offset = 0;   // Calibration offset for AO pin
float A1_Slope = 1; // Calibration slope for A1 pin
int A1_Offset = 0;   // Calibration offset for A1 pin
float A2_Slope = 0.1; // Calibration slope for A1 pin
int A2_Offset = -14;
// You need to define calibration parameters for the new sensor as well
const int redPin = 6;
const int yellowPin = 4;
const int greenPin = 5;

const int interval = 1000; // 1 second

// Set up
void setup() {
  Serial.begin(115200);  // Initialize serial monitor using a baud rate of 115200
  dht1.begin();
  dht2.begin();
  pinMode(redPin, OUTPUT);
  pinMode(yellowPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
}

// Main loop
void loop() {
  Ammonia();
  delay(2000); //
  methane();
  delay(2000); //
  ph();
  delay(1000); //
  temp();
  delay(200); //
  led(redPin);
//  // Blink yellow light
  led(yellowPin);
//  // Blink green light
  led(greenPin);

}



void ph() {
  A2_Out = analogRead(A2_Pin); // Read the analog output measurement sample from the pH sensor's A2 pin
  float calibrated_A2 = A2_Out * A2_Slope + A2_Offset; // Apply calibration
  Serial.print("pH Value: "); // Print out the text "pH Value: "
  Serial.println(calibrated_A2); // Print out the calibrated value
}
void methane() {
  A1_Out = analogRead(A1_Pin); // Read the analog output measurement sample from the MQ4 sensor's A1 pin
  float calibrated_A1 = A1_Out * A1_Slope + A1_Offset; // Apply calibration
  Serial.print("Methane Concentration: "); // Print out the text "Methane Concentration: "
  Serial.println(calibrated_A1); // Print out the calibrated value
}
void Ammonia() {
  AO_Out = analogRead(AO_Pin); // Read the analog output measurement sample from the MQ4 sensor's AO pin
  float calibrated_AO = AO_Out * AO_Slope + AO_Offset; // Apply calibration
  Serial.print("Ammonia Concentration: "); // Print out the text "Ammonia Concentration: "
  Serial.println(calibrated_AO); // Print out the calibrated value
}

void temp() {
  // Read temperature from the first DHT sensor.
  float temperature1 = dht1.readTemperature();
  // Read temperature from the second DHT sensor.
  float temperature2 = dht2.readTemperature();

  // Check if any errors occurred during reading.
  if (!isnan(temperature1)) {
    Serial.print("Temperature from Sensor 1: ");
    Serial.println(temperature1);
    
  } else {
    Serial.println("Failed to read from DHT sensor 1!");
  }

  if (!isnan(temperature2)) {
    Serial.print("Temperature from Sensor 2: ");
    Serial.println(temperature2);
    
  } else {
    Serial.println("Failed to read from DHT sensor 2!");
  }

  // Delay before next reading.
  delay(2000); // Adjust delay as needed.
}

void led(int pin) {
  // Turn the LED on (HIGH is the voltage level)
  digitalWrite(pin, HIGH);
  // Wait for a while
  delay(interval);
  // Turn the LED off by making the voltage LOW
  digitalWrite(pin, LOW);
  // Wait for a while
  delay(interval);
}