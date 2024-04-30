#include <DHT.h>


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
float voltage, phValue, temperature = 25;
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
  {
    static unsigned long timepoint = millis();
    if (millis() - timepoint > 1000U) {  //time interval: 1s
      timepoint = millis();
      //temperature = readTemperature();         // read your temperature sensor to execute temperature compensation
      voltage = analogRead(PH_PIN) / 1024.0 * 5000;  // read the voltage
      phValue = ph.readPH(voltage, temperature);     // convert voltage to pH with temperature compensation
      // Serial.print("temperature:");
      // Serial.print(temperature,1);
      Serial.print("pH value: ");
      Serial.println(phValue, 2);
    }
    ph.calibration(voltage, temperature);  // calibration process by Serail CMD
  }
}

void blinkLED(int pin) {
  digitalWrite(pin, HIGH);
  delay(interval);
  digitalWrite(pin, LOW);
  delay(10000);
}