#include <DHT.h>
#include <SoftwareSerial.h>

#define DHTTYPE DHT11

const int DHT_PIN_1 = 2;
const int DHT_PIN_2 = 3;

DHT dht1(DHT_PIN_1, DHTTYPE);
DHT dht2(DHT_PIN_2, DHTTYPE);

const int methane_sensor = A1;
const float slope_methane = -0.318;
const float intercept_methane = 1.133;
const float baselineResistance_methane = 0.98;

const int ammonia_sensor = A0;
const float slope_ammonia = -0.263;
const float intercept_ammonia = 0.42;
const float baselineResistance_ammonia = 3.37;

#include "DFRobot_PH.h"
#include <EEPROM.h>

#define PH_PIN A2

DFRobot_PH ph;

const int redPin = 6;
const int yellowPin = 4;
const int greenPin = 5;
const int interval = 1000;

SoftwareSerial mySerial(10, 11); // RX, TX

float phValue = 0.0; // Initialize pH value to 0.0

void setup() {
  Serial.begin(115200);
  mySerial.begin(115200); // Start software serial communication
  dht1.begin();
  dht2.begin();
  pinMode(redPin, OUTPUT);
  pinMode(yellowPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  ph.begin();
}

void loop() {
  readAmmonia();
  delay(2000);
  readMethane();
  delay(2000);
  readPH();
  delay(2000);
  readTemperature();
  delay(2000);
  blinkLED(redPin);
  blinkLED(yellowPin);
  blinkLED(greenPin);
}

void readTemperature() {
  float temperature1 = dht1.readTemperature();
  delay(2000);
  float temperature2 = dht2.readTemperature();

  if (!isnan(temperature1)) {
    Serial.print("Temperature Sensor 1: ");
    Serial.println(temperature1);
  } else {
    Serial.println("Failed to read from Temperature Sensor 1!");
  }

  if (!isnan(temperature2)) {
    Serial.print("Temperature Sensor 2: ");
    Serial.println(temperature2);
  } else {
    Serial.println("Failed to read from Temperature Sensor 2!");
  }

  delay(2000);
}

void readMethane() {
  float sensor_volt = analogRead(methane_sensor) * (5.0 / 1023.0);
  float RS_gas = (5.0 - sensor_volt) / sensor_volt;
  float ratio = RS_gas / baselineResistance_methane;
  double ppm_log = (log10(ratio) - intercept_methane) / slope_methane;
  double ppm = pow(10, ppm_log);
  Serial.print("Methane Concentration: ");
  Serial.println(ppm);
  delay(500);
}

void readAmmonia() {
  float sensor_volt = analogRead(ammonia_sensor) * (5.0 / 1023.0);
  float RS_gas = (50.0 / sensor_volt) - 10.0;
  float ratio = RS_gas / baselineResistance_ammonia;
  double ppm_log = (log10(ratio) - intercept_ammonia) / slope_ammonia;
  double ppm = pow(10, ppm_log);
  Serial.print("Ammonia Concentration: ");
  Serial.println(ppm);
  delay(500);
}

void readPH() {
  if (mySerial.available()) { // Check if data is available to read from the sender
    String data = mySerial.readStringUntil('\n'); // Read the incoming data until newline character
    Serial.println(data); // Print the received data on the serial monitor of the receiver

    if (data.startsWith("pH:")) {
      // Extract pH value from the received data
      int index = data.indexOf(":") + 1;
      String pHStr = data.substring(index);
      phValue = pHStr.toFloat();

      // Perform pH-related actions here
      Serial.print("pH Value: ");
      Serial.println(phValue, 2);
    }
  }
}

void blinkLED(int pin) {
  digitalWrite(pin, HIGH);
  delay(interval);
  digitalWrite(pin, LOW);
  delay(interval);
}