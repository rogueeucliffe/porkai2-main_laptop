#include <SoftwareSerial.h>

SoftwareSerial mySerial(10, 11); // RX, TX

float phValue;

void setup()
{
    Serial.begin(115200); // Start the serial monitor
    mySerial.begin(115200); // Start the software serial communication
}

void loop()
{
    if (mySerial.available()) // Check if data is available to read from the sender
    {
        String data = mySerial.readStringUntil('\n'); // Read the incoming data until newline character
        Serial.println(data); // Print the received data on the serial monitor of the receiver

    
        if (data.startsWith("pH:"))
        {
            // Extract pH value from the received data
            int index = data.indexOf(":") + 1;
            String pHStr = data.substring(index);
            phValue = pHStr.toFloat();

            // Perform pH-related actions here
        }
    }

    // Your main loop code can be placed here
}