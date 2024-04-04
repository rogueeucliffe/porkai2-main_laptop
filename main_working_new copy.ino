#include <DHT.h>
#include <Arduino.h>

#define DHTTYPE DHT11

// Pin assignments for DHT sensors.
const int DHT_PIN_1 = 2; // Connect the first sensor to digital pin 2.
const int DHT_PIN_2 = 3; // Connect the second sensor to digital pin 3.

// Create instances of the DHT class for each sensor.
DHT dht1(DHT_PIN_1, DHTTYPE);
DHT dht2(DHT_PIN_2, DHTTYPE);

int methane_sensor = A1; //Sensor pin
float m_methane = -0.318; //Slope
float b_methane = 1.133; //Y-Intercept
float R0_methane = 0.98; //Sensor Resistance in fresh air from previous code

int ammonia_sensor = A0; // Ammonia sensor pin
float m_ammonia = -0.263; // Slope
float b_ammonia = 0.42; // Y-Intercept
float R0_ammonia = 3.37; // Sensor Resistance in fresh air from previous code
                              
int measurings;
float voltage;
float pHvalue;
float b_ph = 0.00;
float m_ph = 0.167;


const int AO_Pin = A0;
const int A1_Pin = A1;
const int A2_Pin = A2; // New pin for pH sensor
int AO_Out; // Declare variable to store AO pin reading
int A1_Out; // Declare variable to store A1 pin reading
int A2_Out; // Declare variable to store A2 pin reading


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
  delay(200); //
  methane();
  delay(200); //
  ph();
  delay(200); //
  temp();
  delay(200); //
  led(redPin);
//  // Blink yellow light
  led(yellowPin);
//  // Blink green light
  led(greenPin);

}



void ph() {
  measurings=0;                                  
  for (int i = 0; i < 10; i++)                   
  {
    measurings = measurings + analogRead(A0);     
    delay(10);                                  
  }
    voltage = ((5 / 1024.0) * (measurings/10)); 
                                                   
    pHvalue = ((7 + ((2.5 - voltage) / m_ph)))+ b_ph;    
    
    Serial.print("pH Value: ");                          
    Serial.println(pHvalue);                          
    delay(1000);                                    
}

void methane() {
  float sensor_volt=0; //Define variable for sensor voltage
  float RS_gas=0; //Define variable for sensor resistance
  float ratio=0; //Define variable for ratio
  float sensorValue = analogRead(methane_sensor); //Read analog values of sensor
  sensor_volt = sensorValue * (5.0 / 1023.0); //Convert analog values to voltage
  RS_gas = ((5.0 * 1.0) / sensor_volt) - 1.0; //Get value of RS in a gas
  ratio = RS_gas / R0_methane;   // Get ratio RS_gas/RS_air

  double ppm_log = (log10(ratio) - b_methane) / m_methane; //Get ppm value in linear scale according to the the ratio value
  double ppm = pow(10, ppm_log); //Convert ppm value to log scale
  double percentage = ppm / 10000; //Convert to percentage
  Serial.print("Methane Concentration: ");
  Serial.println(percentage); //Load screen buffer with percentage value
  delay(500);
}
void Ammonia() {
  float sensor_volt_ammonia; // Define variable for sensor voltage
  float RS_Gas_ammonia; // Define variable for sensor resistance
  float ratio_ammonia; // Define variable for ratio_ammonia
  float sensorValue = analogRead(ammonia_sensor); // Read analog values of sensor
  sensor_volt_ammonia = sensorValue * (5.0 / 1023.0); // Convert analog values to voltage
  RS_Gas_ammonia = ((5.0 * 10.0) / sensor_volt_ammonia) - 10.0; // Get value of RS in a gas
  ratio_ammonia = RS_Gas_ammonia / R0_ammonia; // Get ratio_ammonia RS_gas/RS_air

  double ppm_log = (log10(ratio_ammonia) - b_ammonia) / m_ammonia; // Get ppm value in linear scale according to the ratio value
  double ppm = pow(10, ppm_log); // Convert ppm value to log scale

  Serial.print("Ammonia Concentration: ");
  Serial.println(ppm);
  
  delay(500); // Delay before next reading
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