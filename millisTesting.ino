/**********************************************************
 *  millisTesting.ino                                     *
 *      Written By: Thomas C. Smith                       *
 *              On: 20210123                              *
 **********************************************************
 *  Shows one way to make a NON-BLOCKING delay.           *
 *  The Arduino 'delay()' function halts all processing   *
 *    until the delay is over so it is a BLOCKING function*
 *    and prevents other code from continuing.            *
 **********************************************************
 *  Notes                                                 *
 *  The millis() function must use unsigned long data     *
 *    type and it rolls back to zero again in approx      *
 *    48 days.                                            *
 **********************************************************/
/**********************************************************
 * User changable variables                               *
 **********************************************************/
float delayInSeconds      = 10.0;
/**********************************************************
*  Don't change these variables unless you know what you  *
*     are doing.                                          *
***********************************************************/
unsigned long startCount  = 0;
unsigned long trigger     = delayInSeconds * 1000;
unsigned long incrament   = trigger;
/**********************************************************
 *  End of program variables                              *
 **********************************************************/

/**********************************************************
 *  User functions (I place them at the beginning as some *
 *    compilers complain if otherwise.)                   *
 **********************************************************/
unsigned long doAlert(unsigned long theCount){
  // This function just prints out to the serial monitor
  // that a timing alert happend using the millis() function
  Serial.print("Alert!!! Current count: " + String(theCount) + " starting count: " + String(startCount));
  startCount = trigger;
  // reset the 'trigger' value
  trigger = theCount + incrament;
  Serial.println(" -> Next trigger count: " + String(trigger));
}
/************************************************************
 *  End of user functions                                   *
 ************************************************************/
 
void setup(){
  Serial.begin(9600);
  Serial.println("Starting the tutorial");
}
void loop(){
  unsigned long Now = millis();
//  Serial.println("Now: " + String(Now));                // uncomment to watch counts build
//  Serial.println("Now + trigger: " + String(trigger));  // uncomment to watch counts build
  if (Now >= trigger){
    doAlert(Now);
  }
  // DO OTHER STUFF HERE
  //delay(999);  // uncomment to insert a delay for watching counts build
}
