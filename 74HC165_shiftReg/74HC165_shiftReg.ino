/**************************************************************
 *    74CH165_shiftReg.ino                                    *
 *    Written By: Thomas C. Smith                             *
 *            On: 20210212                                    *
 **************************************************************
 *    Purpose                                                 *
 *    - This is a simple sketch showing how to increase the   *
 *    digital IO inputs using an 74CH165 Serial Register.     *
 **************************************************************
 *    Pinouts                                                 *
 *    Arduino     74CH595         Notes                       *
 *    ---------   --------------  --------------------------- *
 *    5VDC        Pin 16          VCC on 74CH595              *
 *    GND         Pins 8 & 13     GND & OE (output enable)    *
 *    VCC -> GND  100 uF cap.     Smoothing DC                *
 *    D10         Pin 12          ST_CP (store reg clk in)    *
 *    D11         Pin 11          SH_CP (shift reg clk in)    *
 *    D12         Pin 14          DS (data serial input)      *
 *                                                            *
 *    74CH595     LEDs            Notes                       *
 *    ---------   --------------  --------------------------- *
 *    Pin 15      Q0 LED          Use a 220-470 Ohm resistore *
 *    Pin 1       Q1 LED                                      *
 *    Pin 2       Q2 LED                                      *
 *    Pin 3       Q3 LED                                      *
 *    Pin 4       Q4 LED                                      *
 *    Pin 5       Q5 LED                                      *
 *    Pin 6       Q6 LED                                      *
 *    Pin 7       Q7 LED                                      *
 **************************************************************
 *    Notes                                                   *
 *    - Place support functions before the setup() to make    *
 *       the program useable in other IDEs like PlatformIO.   *
 *                                                            *
 **************************************************************/
/**************************************************************
 *    Support Functions                                       *
 *    FuncName                Purpose                         *
 *    ----------------------  ------------------------------- *
 **************************************************************/

/**************************************************************
 *     End of Support Functions                               *
 **************************************************************/

 
/**************************************************************
 *    Global Variables                                        *
 **************************************************************/ 
// Define Connections to 74HC165
 
// PL pin 1
int load = 7;
// CE pin 15
int clockEnablePin = 4;
// Q7 pin 7
int dataIn = 5;
// CP pin 2
int clockIn = 6;
 
 /*************************************************************
  *   End of Global Variables                                 *
  *************************************************************/
  
void setup() {
  // Setup Serial Monitor
  Serial.begin(9600);
 
  // Setup 74HC165 connections
  pinMode(load, OUTPUT);
  pinMode(clockEnablePin, OUTPUT);
  pinMode(clockIn, OUTPUT);
  pinMode(dataIn, INPUT);
}

void loop()
{
 
  // Write pulse to load pin
  digitalWrite(load, LOW);
  delayMicroseconds(5);
  digitalWrite(load, HIGH);
  delayMicroseconds(5);
 
  // Get data from 74HC165
  digitalWrite(clockIn, HIGH);
  digitalWrite(clockEnablePin, LOW);
  byte incoming = shiftIn(dataIn, clockIn, MSBFIRST);
  digitalWrite(clockEnablePin, HIGH);
 
  // Print to serial monitor
  Serial.print("Pin States:\t");
  Serial.println(~incoming, BIN);
  delay(200);
}
