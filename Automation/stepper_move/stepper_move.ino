/*This Sketch moves a 28BYJ-48 stepper motor to a specific position
 * Inputs are: integer entwered through the Serial Read funmction
 * the command structure is: NNNN <CR> for CCW rotation or -NNNN<CR> for CW rotation in addition
 * if the command Z<CR> is entered the present position of the 
 * stepper is considered the zero position. All movement is ended with the motor
 * rotating in the CW direction.
 * 
 * Author: Jerry Foote
 * Version 1.0
 * April 9, 2020* 
 * 
 */
int value = 0;
const int overShoot = 100;
int sign = 1;
int lastPos = 0;

#include <Stepper.h>

const int stepsPerRevolution = 2048;
int currentPos = 0;
int newPosition = 0;

Stepper myStepper = Stepper(stepsPerRevolution, 8, 10, 9, 11);

void setup() {
  Serial.begin(9600);
  Serial.println("<Arduino is ready>");
  myStepper.setSpeed(5);

}
void loop()
{

  if ( Serial.available())
  {

    char ch = Serial.read();

    if (ch >= '0' && ch <= '9') // is this an ascii digit between 0 and 9?

      value = (value * 10) + (ch - '0'); // yes, accumulate the value

    else if ( ch == '-')

      sign = -1;
    else if (ch == 'Z' || ch == 'z') {
      Serial.println("Setting position to zero");
      currentPos = 0;
      newPosition = 0;
      
    }

    else // this assumes any char not a digit or minus sign or a 'z' terminates the value

    {

      value = value * sign ;  // set value to the accumulated value
      newPosition = value;
      myStepper.step(newPosition - currentPos + overShoot);
      Serial.println(newPosition - currentPos + overShoot);
      delay(1000);
      myStepper.step(-overShoot);
      //Serial.println(newPosition);
      currentPos = newPosition;



      Serial.println(currentPos);
      Serial.println(newPosition);
      value = 0; // reset value to 0 ready for the next sequence of digits

      sign = 1;

    }

  }

}
