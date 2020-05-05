/*
 * This sketch is designed to demonstrate the step functions
 * using a 4-wire bipolar stepper motor. A related sketch will
 * use the ULN2003 stepper driver instead of just the Arduino.
 * This is an example of simple "Wave Driving"
 */

 // Variables
 #define STEPPER_PIN_1  8
 #define STEPPER_PIN_2  9
 #define STEPPER_PIN_3  10
 #define STEPPER_PIN_4  11
 int step_number = 0;     // keeps track of the step count
 int theDelay = 10;        // global delay in milliseconds
// boolean dir = true;    // keeps track of the current direction
// byte charIn = 49;      // holds the value read on the serial bus
// int speed = 100;       // speed of the stepper, initial is MAX of 10

void setup() 
{
  pinMode(STEPPER_PIN_1, OUTPUT);
  pinMode(STEPPER_PIN_2, OUTPUT);
  pinMode(STEPPER_PIN_3, OUTPUT);
  pinMode(STEPPER_PIN_4, OUTPUT);
  //Serial.begin(9600);
}

void loop() 
{
  for(int a = 0; a < 200; a++)  // 15 deg/step = 360/15=24 iterations for one rev
  {
    OneStep(false);   //CW
    delay(theDelay);
  }
  for (int a = 0; a < 200; a++)
  {
    OneStep(true);    // CCW
    delay(theDelay);
  }
}

void OneStep(bool dir)
{
  if(dir == true) // CW
  {
    switch (step_number)
    {
      case 0:
        digitalWrite(STEPPER_PIN_1,HIGH);
        digitalWrite(STEPPER_PIN_2,LOW);
        digitalWrite(STEPPER_PIN_3,LOW);
        digitalWrite(STEPPER_PIN_4,LOW);
        break;
      case 1:
        digitalWrite(STEPPER_PIN_1,LOW);
        digitalWrite(STEPPER_PIN_2,HIGH);
        digitalWrite(STEPPER_PIN_3,LOW);
        digitalWrite(STEPPER_PIN_4,LOW);
        break;
      case 2:
        digitalWrite(STEPPER_PIN_1,LOW);
        digitalWrite(STEPPER_PIN_2,LOW);
        digitalWrite(STEPPER_PIN_3,HIGH);
        digitalWrite(STEPPER_PIN_4,LOW);
        break;
       case 3:
        digitalWrite(STEPPER_PIN_1,LOW);
        digitalWrite(STEPPER_PIN_2,LOW);
        digitalWrite(STEPPER_PIN_3,LOW);
        digitalWrite(STEPPER_PIN_4,HIGH);
        break;
    }
  }
    else  // CCW
    {
      switch(step_number)
      {
        case 0:
          digitalWrite(STEPPER_PIN_1,LOW);
          digitalWrite(STEPPER_PIN_2,LOW);
          digitalWrite(STEPPER_PIN_3,LOW);
          digitalWrite(STEPPER_PIN_4,HIGH);
          break;
        case 1:
          digitalWrite(STEPPER_PIN_1,LOW);
          digitalWrite(STEPPER_PIN_2,LOW);
          digitalWrite(STEPPER_PIN_3,HIGH);
          digitalWrite(STEPPER_PIN_4,LOW);
          break;
        case 2:
          digitalWrite(STEPPER_PIN_1,LOW);
          digitalWrite(STEPPER_PIN_2,HIGH);
          digitalWrite(STEPPER_PIN_3,LOW);
          digitalWrite(STEPPER_PIN_4,LOW);
          break;
        case 3:
          digitalWrite(STEPPER_PIN_1,HIGH);
          digitalWrite(STEPPER_PIN_2,LOW);
          digitalWrite(STEPPER_PIN_3,LOW);
          digitalWrite(STEPPER_PIN_4,LOW);
          break;
    }
  }
  step_number++;
  if (step_number > 24)
  {
    step_number = 0;
  }
  delay(theDelay);
}
