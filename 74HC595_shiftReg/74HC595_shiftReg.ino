/**************************************************************
 *    74CH595_shiftReg.ino                                    *
 *    Written By: Thomas C. Smith                             *
 *            On: 20210212                                    *
 **************************************************************
 *    Purpose                                                 *
 *    - This is a simple sketch showing how to increaswe the  *
 *    digital IO outputs using an 74CH595 Serial Register.    *
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
// Define Connections to 74HC595
 
// ST_CP pin 12
const int latchPin = 10;
// SH_CP pin 11
const int clockPin = 11;
// DS pin 14
const int dataPin = 12;
 
 /*************************************************************
  *   End of Global Variables                                 *
  *************************************************************/
  
void setup() {
  Serial.begin(9600);
  pinMode(latchPin,  OUTPUT);
  pinMode(clockPin,  OUTPUT);
  pinMode(dataPin,   OUTPUT);

}

void loop() {
  // Count from 0 to 255 and display in binary
 
  for (int numberToDisplay = 0; numberToDisplay < 256; numberToDisplay++) {
 
    // ST_CP LOW to keep LEDs from changing while reading serial data
    digitalWrite(latchPin, LOW);
 
    // Shift out the bits
    shiftOut(dataPin, clockPin, MSBFIRST, numberToDisplay);
 
    // ST_CP HIGH change LEDs
    digitalWrite(latchPin, HIGH);

    // build the string output for the serial monitor
    String newNumberToDisplay = String(numberToDisplay,BIN);
    int lenDigits = newNumberToDisplay.length();
    newNumberToDisplay = ("00000000" + newNumberToDisplay).substring(lenDigits);

    // print out the string just built into the serial monitor
    Serial.print("Number:\tDEC: " + String(numberToDisplay) + "\tBIN: ");
    Serial.print(newNumberToDisplay);
    Serial.println("\tHEX: " + String(numberToDisplay, HEX));

    delay(500);
  }
}
