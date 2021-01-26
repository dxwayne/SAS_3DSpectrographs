/**********************************************************
 *  interruptTesting.ino                                     *
 *      Written By: Thomas C. Smith                       *
 *              On: 20210123                              *
 **********************************************************
 *  Shows how to use Arduino interrupts.                  *
 **********************************************************
 *  Notes                                                 *
 *  The Arduino Uno and Nano and their ilks have pins     *
 *    designed for use as interrupts. An interrupt halts  *
 *    the current program code running and jumps to the   *                                           
 *    specified function, does it's work and then         *
 *    optionally, returns to where the interrup stopped   *
 *    the code in the main function, the 'loop'.          *
 *  The interrupt pins on the Arduino Uno are as follows: *
 *  Board  Digital Pins Usable For Interrupts             *
 *    - Uno, Nano, Mini, other 328-based  2, 3            *
 *    - Mega, Mega2560, MegaADK 2, 3, 18, 19, 20, 21      *
 *    - Micro, Leonardo, other 32u4-based 0, 1, 2, 3, 7   *
 *    - Zero  all digital pins, except 4                  *
 *    - Due all digital pins                              *
 **********************************************************
 *    Pinout                                              *
 *    Arduino   Pushbutton switch                         *
 *    -------   -----------------                         *
 *    D3        One side to ground, other to +5 VDC       *
 *    D4        To dropping resistor to GND               *
 **********************************************************/
 
/**********************************************************
 * User changable variables                               *
 **********************************************************/
const int interruptPin  = 3;    // interrupt trigger pin
const int led           = 13;   // built-in LED

/**********************************************************
 *  End of user changable variables                       *
 **********************************************************/
 
/**********************************************************
 *  Program variables                                     *
 *  Don't change these variables unless you know what you *
 *     are doing.                                         *
 **********************************************************/
volatile bool eventTriggered = false; // demo code for interrupt variables
/**********************************************************
 *  End of program variables                              *
 **********************************************************/

/**********************************************************
 *  User functions (I place them at the beginning as some *
 *    compilers complain if otherwise.)                   *
 **********************************************************/
void event(){
  // function to demonstrate an interrupt
  if (eventTriggered == false){      // LED is off
    // is now false so set it true
    eventTriggered = true;          // just sets a variable value
  }
  else {
    // is now true so set it false
    eventTriggered = false;         // just sets a variable value
  }
  Serial.println("Interrupt triggered...");
  delayMicroseconds(100);           // short pause to take care of switch bounce
}

/************************************************************
 *  End of user functions                                   *
 ************************************************************/

void setup() {
  // reenable interrupts if they were disabled
  interrupts();
  pinMode(interruptPin, INPUT_PULLUP);  // kept HIGH until triggered
                                        // like when using a button
  pinMode(led, OUTPUT);                 // onboard LED pin
  attachInterrupt(digitalPinToInterrupt(interruptPin), event, LOW);
  Serial.begin(9600);
  Serial.println("Beginning interrupt tutorial");
}

void loop() {
  // running program that awaites an interrupt on the assigned pin
 
  // we will use the onboard LED as the running program
  digitalWrite(led, HIGH);    // turn it on
  delay(500);                 // short delay for a blink
  digitalWrite(led, LOW);     // turn it off
  delay(500);                 // another short delay
}
