#include <DFRobot_DHT11.h>
DFRobot_DHT11 DHT;
#define DHT11_PIN 10



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

// Set up
void setup() {
  Serial.begin(115200);  // Initialize serial monitor using a baud rate of 115200
}

// Main loop
void loop() {
  Ammonia();
  delay(200); //
  methane();
  delay(200); //
  ph();
  delay(200); //
  temp1();
  delay(200); //

  delay(5000); //

}

void temp1() {
  DHT.read(DHT11_PIN);
  Serial.print("temp 1: ");
  Serial.println(DHT.temperature);
  //  Serial.print("  humi:");
  //  Serial.println(DHT.humidity);
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