/*
  This sketch controlls the movement of the cal/flat mirror in the LowSpec spectrograph.

  When the switch is high (pin 2 = +V the motor will run CW pushing the mirror in 10mm into the light
  path and allow the cal/flat illumination to enter the slit.

    When the switch is Low = Gnd the motor will run CCW and the mirror will withdraw from the light path.

  Author: Jerry Foote

  Initial date March 16, 2020
*/





const int  switchPin = 2;    // the pin that the switch is attached to
int switchState = 0;         // current state of the switch
int lastswitchState = 0;     // previous state of the switch

// Include the AccelStepper library:
#include <AccelStepper.h>
// Motor pin definitions:
#define motorPin1  8      // IN1 on the ULN2003 driver
#define motorPin2  9      // IN2 on the ULN2003 driver
#define motorPin3  10     // IN3 on the ULN2003 driver
#define motorPin4  11     // IN4 on the ULN2003 driver
// Define the AccelStepper interface type; 4 wire motor in half step mode:
#define MotorInterfaceType 8
// Initialize with pin sequence IN1-IN3-IN2-IN4 for using the AccelStepper library with 28BYJ-48 stepper motor:
AccelStepper stepper = AccelStepper(MotorInterfaceType, motorPin1, motorPin3, motorPin2, motorPin4);

void setup() {
  // initialize the switch pin as a input:
  pinMode(switchPin, INPUT);
  // initialize serial communication:
  Serial.begin(9600);
  // Set the maximum steps per second:
  stepper.setMaxSpeed(2000);

}


void loop() {
  // read the switch input pin:
  switchState = digitalRead(switchPin);

  // compare the switchState to its previous state
  if (switchState != lastswitchState) {
    if (switchState == HIGH) {
      // if the current state is HIGH then the switch went from off to on:
      Serial.println("on");
      // Reset the position to 0:
      stepper.setCurrentPosition(0);
      // Run the motor backwards at 1000 steps/second until the motor reaches -26624 steps (6.6 revolutions):
      while (stepper.currentPosition() != -26624) {
        stepper.setSpeed(-1000);
        stepper.runSpeed();
      }
    } else {
      // if the current state is LOW then the switch went from on to off:
      Serial.println("off");
      // Reset the position to 0:
      stepper.setCurrentPosition(0);
      // Run the motor forward at 1000 steps/second until the motor reaches 26624 steps (6.6 revolutions):
      while (stepper.currentPosition() != 26624) {
        stepper.setSpeed(1000);
        stepper.runSpeed();

      }
      // Delay a little bit to avoid bouncing
      delay(50);
    }
    // save the current state as the last state, for next time through the loop
    lastswitchState = switchState;

  }
}
