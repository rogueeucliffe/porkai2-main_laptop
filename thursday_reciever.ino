#include <DHT.h>


#define DHTTYPE DHT11

const int DHT_PIN_1 = 2;
const int DHT_PIN_2 = 3;

DHT dht1(DHT_PIN_1, DHTTYPE);
DHT dht2(DHT_PIN_2, DHTTYPE);



//https://github.com/miguel5612/MQSensorsLib_Docs/

#include <MQUnifiedsensor.h>
/************************Hardware Related Macros************************************/
#define Board ("Arduino UNO")
#define Pin (A1)  //Analog input 4 of your arduino
/***********************Software Related Macros************************************/
#define Type ("MQ-4")  //MQ4
#define Voltage_Resolution (5)
#define ADC_Bit_Resolution (10)  // For arduino UNO/MEGA/NANO
#define RatioMQ4CleanAir (4.4)   //RS / R0 = 60 ppm
/*****************************Globals***********************************************/
//Declare Sensor
MQUnifiedsensor MQ4(Board, Voltage_Resolution, ADC_Bit_Resolution, Pin, Type);


//https://github.com/carry0987/MQ-137/blob/master/mq-137.ino
#define RL 47         //The value of resistor RL is 47K
#define m -0.263      //Enter calculated Slope
#define b 0.42        //Enter calculated intercept
#define Ro 20         //Enter found Ro value
#define MQ_sensor A0  //Sensor is connected to A4



const int redPin = 6;
const int yellowPin = 4;
const int greenPin = 5;
const int interval = 1000;

String inputString = "";  // a string to hold incoming data

float phValue = 0.0;  // Initialize pH value to 0.0

void setup() {
  Serial.begin(115200);
  MQ4.setRegressionMethod(1);  //_PPM =  a*ratio^b
  MQ4.setA(1012.7);
  MQ4.setB(-2.786);  // Configure the equation to to calculate CH4 concentration

  dht1.begin();
  dht2.begin();
  pinMode(redPin, OUTPUT);
  pinMode(yellowPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  MQ4.init();

  Serial.print("Calibrating please wait.");
  float calcR0 = 0;
  for (int i = 1; i <= 10; i++) {
    MQ4.update();  // Update data, the arduino will read the voltage from the analog pin
    calcR0 += MQ4.calibrate(RatioMQ4CleanAir);
    Serial.print(".");
  }
  MQ4.setR0(calcR0 / 10);
  Serial.println("  done!.");

  if (isinf(calcR0)) {
    Serial.println("Warning: Conection issue, R0 is infinite (Open circuit detected) please check your wiring and supply");
    while (1)
      ;
  }
  if (calcR0 == 0) {
    Serial.println("Warning: Conection issue found, R0 is zero (Analog pin shorts to ground) please check your wiring and supply");
    while (1)
      ;
  }
  /*****************************  MQ CAlibration ********************************************/
  MQ4.serialDebug(true);
}

void loop() {
  readAmmonia();
  // delay(1000);
  readMethane();
  // delay(2000);
  readPH();
  // delay(1000);
  readTemperature();
  // delay(1000);
  // blinkLED(redPin);
  // blinkLED(yellowPin);
  // blinkLED(greenPin);
}

void readTemperature() {
  float temperature1 = dht1.readTemperature();
  // delay(2000);
  float temperature2 = dht2.readTemperature();

  if (!isnan(temperature1)) {
    Serial.print("Temperature Sensor 1: ");
    Serial.println(temperature1);
  } else {
    Serial.println("Failed to read from Temperature Sensor 1!");
  }

  //  if (!isnan(temperature2)) {
  //    Serial.print("Temperature Sensor 2: ");
  //    Serial.println(temperature2);
  //  } else {
  //    Serial.println("Failed to read from Temperature Sensor 2!");
  //  }

  // delay(2000);
}

void readMethane() {
  MQ4.update();  // Update data, the arduino will read the voltage from the analog pin
  float CH4 = MQ4.readSensor();
  Serial.print("Methane Concentration: ");
  Serial.println(CH4);
}



void readAmmonia() {
  float VRL;                                      //Voltage drop across the MQ sensor
  float Rs;                                       //Sensor resistance at gas concentration
  float ratio;                                    //Define variable for ratio
  VRL = analogRead(MQ_sensor) * (5.0 / 1023.0);   //Measure the voltage drop and convert to 0-5V
  Rs = ((5.0 * RL) / VRL) - RL;                   //Use formula to get Rs value
  ratio = Rs / Ro;                                // find ratio Rs/Ro
  float ppm = pow(10, ((log10(ratio) - b) / m));  //use formula to calculate ppm
  Serial.print("Ammonia Concentration: ");
  Serial.println(ppm);

  delay(200);
}




bool newData = false;    // flag to indicate if new data has been received

void readPH() {
  // Check if data is available to read from serial
  if (Serial.available() > 0) {
    // Read the incoming byte
    char incomingByte = Serial.read();
    
    // Check if the received byte is the start of the message
    if (incomingByte == 'p') {
      inputString = "";  // Clear the input string if it's a new message
      newData = true;    // Set the flag to indicate new data has been received
    }
    
    // Add the incoming byte to the inputString
    inputString += incomingByte;

    // Check if the end of the message is reached
    if (incomingByte == '\n' && newData) {
      // Extract pH value from the received string
      float pHValue = inputString.substring(inputString.indexOf(':') + 1).toFloat();
      Serial.print("pH Value: ");
      Serial.println(pHValue);
      
      // Reset the flags and input string for the next message
      newData = false;
      inputString = "";
    }
  }
}



void blinkLED(int pin) {
  digitalWrite(pin, HIGH);
  delay(interval);
  digitalWrite(pin, LOW);
  delay(interval);
}