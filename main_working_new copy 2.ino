#include <DHT.h>
#include <Arduino.h>

#define DHTTYPE DHT11

const int DHT_PIN_1 = 2;
const int DHT_PIN_2 = 3;

DHT dht1(DHT_PIN_1, DHTTYPE);
DHT dht2(DHT_PIN_2, DHTTYPE);

const int methane_sensor = A1;
const float m_methane = -0.318;
const float b_methane = 1.133;
const float R0_methane = 0.98;

const int ammonia_sensor = A0;
const float m_ammonia = -0.263;
const float b_ammonia = 0.42;
const float R0_ammonia = 3.37;

#include "DFRobot_PH.h"
#include <EEPROM.h>

#define PH_PIN A2
float voltage,phValue,temperature = 31;
DFRobot_PH ph;

const int redPin = 6;
const int yellowPin = 4;
const int greenPin = 5;
const int interval = 1000;

void setup() {
  Serial.begin(115200);
  dht1.begin();
  dht2.begin();
  pinMode(redPin, OUTPUT);
  pinMode(yellowPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  ph.begin();
}

void loop() {
  readAmmonia();
  delay(200);
  readMethane();
  delay(200);
  readPH();
  delay(200);
  readTemperature();
  delay(200);
  blinkLED(redPin);
  blinkLED(yellowPin);
  blinkLED(greenPin);
}

void readTemperature() {
  float temperature1 = dht1.readTemperature();
  float temperature2 = dht2.readTemperature();

  if (!isnan(temperature1)) {
    Serial.print("temp 2:");
    Serial.println(temperature1);
  } else {
    Serial.println("Failed to read from DHT sensor 1!");
  }

  if (!isnan(temperature2)) {
    Serial.print("temp 1:");
    Serial.println(temperature2);
  } else {
    Serial.println("Failed to read from DHT sensor 2!");
  }

  delay(2000);
}

void readMethane() {
  // Read analog voltage from methane sensor
  float sensor_volt = analogRead(methane_sensor) * (5.0 / 1023.0);

  // Calculate resistance of the sensor (RS_gas)
  // Note: For a 5V sensor, we assume it behaves linearly over its entire range
  float RS_gas = (5.0 - sensor_volt) / sensor_volt;

  // Calculate ratio
  float ratio = RS_gas / R0_methane;

  // Calculate ppm using calibration parameters
  double ppm_log = (log10(ratio) - b_methane) / m_methane;
  double ppm = pow(10, ppm_log);

  // Print methane concentration in ppm
  Serial.print("Methane Concentration: ");
  Serial.println(ppm);

  // Delay for stability
  delay(500);
}


void readAmmonia() {
  float sensor_volt = analogRead(ammonia_sensor) * (5.0 / 1023.0);
  float RS_gas = (50.0 / sensor_volt) - 10.0;
  float ratio = RS_gas / R0_ammonia;
  double ppm_log = (log10(ratio) - b_ammonia) / m_ammonia;
  double ppm = pow(10, ppm_log);
  Serial.print("Ammonia Concentration: ");
  Serial.println(ppm);
  delay(500);
}

void readPH() {
  unsigned long int avgValue = 0;

  for (int i = 0; i < numSamples; i++) {
    sensorValues[i] = analogRead(pH_sensor);
    delay(10);
  }

  for (int i = 0; i < numSamples - 1; i++) {
    for (int j = i + 1; j < numSamples; j++) {
      if (sensorValues[i] > sensorValues[j]) {
        int temp = sensorValues[i];
        sensorValues[i] = sensorValues[j];
        sensorValues[j] = temp;
      }
    }
  }

  for (int i = 2; i < numSamples - 2; i++) {
    avgValue += sensorValues[i];
  }

  float voltage = avgValue * 5.0 / 1024 / (numSamples - 4);
  float pHValue = -5.70 * voltage + calibration_value;

  Serial.print("pH Value: ");
  Serial.println(pHValue);

  delay(1000);
}

void readPH(){
    static unsigned long timepoint = millis();
    if(millis()-timepoint>1000U){                  //time interval: 1s
        timepoint = millis();
        //temperature = readTemperature();         // read your temperature sensor to execute temperature compensation
        voltage = analogRead(PH_PIN)/1024.0*5000;  // read the voltage
        phValue = ph.readPH(voltage,temperature);  // convert voltage to pH with temperature compensation
        // Serial.print("temperature:");
        // Serial.print(temperature,1);
        Serial.print("pH Value: ");
        Serial.println(phValue,2);
        // Serial.print("^C  pH:");
        // Serial.println(phValue,2);
    }
    ph.calibration(voltage,temperature);           // calibration process by Serail CMD
}

float readTemperature()
{
  //add your code here to get the temperature from your temperature sensor
}

void blinkLED(int pin) {
  digitalWrite(pin, HIGH);
  delay(interval);
  digitalWrite(pin, LOW);
  delay(interval);
}