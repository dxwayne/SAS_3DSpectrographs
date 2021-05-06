/****************************************************************
 *  interruptTesting.ino                                        *
 *     Modified By: Thomas C. Smith                             *
 *              On: 20210123                                    *
 * https://www.electronicshub.org/arduino-interrupts-tutorial/  *
 * is a source for this code.                                   *
 ****************************************************************
 *  Changes                                                     *
 *  20210209 - Modified the sketch to use an external LED       *
 *      to show the interrupt routine running visually.         *
 *  20210214 rebuilt the code using the above reference to use  *
 *      the millis() function for button debaounce.             *
 ****************************************************************
 *  Notes                                                       *
 *  The Arduino Uno and Nano and their ilks have pins           *
 *    designed for use as interrupts. An interrupt halts        *
 *    the current program code running and jumps to the         *                                            
 *    specified function, does it's work and then               *
 *    optionally, returns to where the interrup stopped         *
 *    the code in the main function, the 'loop'.                *
 *  The interrupt pins on the Arduino Uno are as follows:       *
 *  Board  Digital Pins Usable For Interrupts                   *
 *    - Uno, Nano, Mini, other 328-based  2, 3                  *
 *    - Mega, Mega2560, MegaADK 2, 3, 18, 19, 20, 21            *
 *    - Micro, Leonardo, other 32u4-based 0, 1, 2, 3, 7         *
 *    - Zero  all digital pins, except 4                        *
 *    - Due all digital pins                                    *
 ****************************************************************
 *    Pinout                                                    *
 *    Arduino   Pushbutton switch                               *
 *    -------   -----------------                               *
 *    D3        One side to ground, other to pin 4              *
 *    D4        To dropping resistor (270 Ohm but anything      *
 *                 between 270 and 470 Ohms is fine) to GND.    *
 ****************************************************************/
 
/********************************************
 * User changable variables                 *
 ********************************************/
int interruptPin  = 4;          // This is the interrupt indicating LED pin.
int onboardLED    = 13;         // Built-in LED.
int buttonPin     = 2;          // Interrupt pin.

int ledToggle;                  // Used to decide what state the interrupt LED should be in.
int previousState = HIGH;       // Used to set the current requested state.
unsigned int previousPress;     // Holds the time of the last button press used aginst curreten millis().
volatile int buttonFlag;        // Flag used in the ISR to toggle the interrupt pin.
int buttonDebounce = 20;        // Time in milliseconds for debouce delay.

/*********************************************
 *  End of user changable variables          *
 *********************************************/
 
/*********************************************
 *  Program variables                        *
 *  Don't change these variables unless you  *
 *  know what you are doing.                 *
 *********************************************/

/**********************************************
 *  End of program variables                  *
 **********************************************/

/**********************************************
 *  User functions (I place them at the       *
 *  beginning as some compilers complain if   *
 *  otherwise.)                               *
 **********************************************/
void button_ISR(){
  buttonFlag = 1;                 // Flag used to toggle interruptPin
                                  // this is about a short as one can make an ISR.
}

/**********************************************
 *  End of user functions                     *
 **********************************************/

void setup() 
{
  pinMode(interruptPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(2), button_ISR, CHANGE);
}

void loop() 
{
  if((millis() - previousPress) > buttonDebounce && buttonFlag)
  {
    previousPress = millis();
    if(digitalRead(buttonPin) == LOW && previousState == HIGH)
    {
      ledToggle =! ledToggle;     // This toggles the interrupt LED action.
      digitalWrite(interruptPin, ledToggle);
      previousState = LOW;
    }
    
    else if(digitalRead(buttonPin) == HIGH && previousState == LOW)
    {
      previousState = HIGH;
    }
    buttonFlag = 0;               // Resets the flag making it ready for the next button press.
  }
  // The following code continuously turns the onboard LED on and off to simulate other code that
  // is run. There is a small timing penalty between flashes when the IRS is called.
  digitalWrite(onboardLED, HIGH);
  delay(100);
  digitalWrite(onboardLED, LOW);
  delay(100);
}
