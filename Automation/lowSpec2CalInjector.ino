///**************************************************
// *            lowSpec2CalInjector.ino             *
// **************************************************
// *      Written by: Thomas C. Smtih               *
// *      Created on: 20200323                      *
// **************************************************
// *    Revision history:                           *
// *    - Initial relase, version 1.0               *
// *    - 20200324 decided to create using standard *
// *      stepper driver instead of AccelStepper    *
// *    - 20200731 modified the slit lamp off       *
// *      from '9' to '7' so numerics are in order. *
// *      Added more info to the status command.    *
// *      Created a listing of functions.           *
// *    - 20200806 repaired the serial comms        *
// **************************************************/

///**************************************************
// *    Functions:   (In coded order)               *
// **************************************************
// *    homeMotor()                                 *
// *    toggleAutoHome()                            *
// *    driveIN()                                   *
// *    driveOUT()                                  *
// *    runTo()                                     *
// *    resetCurrentStep()                          *
// *    doCommandEvaluation()                       *
// *    getStep()
// *    getStatus()                                 *
// *    doAction()                                  *
// *    serialEvent()                               *
// *    showHelp()                                  *
// *    setup()                                     *
// *    loop()                                      *
// **************************************************/

///**************************************************
// *            Serial Command Protocol             *
// **************************************************
// *  A = toggle AutoHome feature                   *
// *  H = home the injector                         *
// *  L = toggle LOCAL commands for serial ECHO     *
// *  I = drive inward, CW from above motor shatf   *
// *  O = drive outward, CCW from above motor shaft *
// *  M = move  to the position value sent          *
// *  C = cal lamp relay ON                         *
// *  5 = cal lamp relay OFF                        *
// *  F = flat lamp relay ON                        *
// *  6 = flat lamp relay OFF                       *
// *  S = slit lamp LED ON                          *
// *  7 = slit lamp LED OFF                         *
// *  R = change speed of motor                     *
// *  T = test all three lamps                      *
// *  Z = reset the zero point w/ homing            *
// *  0 = (zero) get step                           *
// *  ? = brief help on commands                    *
// *************************************************/

///**************************************************
// *                Arduino Pinout                  *
// **************************************************
// *  1)  Injector Stepper Motor                    *
// *      Arduino   ->  ULN2003 Driver              *
// *      -------       --------------              *
// *     Ext.+5VDC  ->  (+) 5-12 pin                *
// *        GND     ->  (-) 5-12 pin                *
// *        D8      ->  ULN2003 IN1                 *
// *        D9      ->  ULN2003 IN2                 *
// *        D10     ->  ULN2003 IN3                 *
// *        D11     ->  ULN2003 IN4                 *
// *  - - - - - - - - - - - - - - - - - - - - - - - *
// *  2)  Lamp Relay Module                         *
// *      Arduino   ->  Relay Board                 *
// *      -------       ---------------             *
// *        +5 VDC  ->  Relay VCC                   *
// *        GND     ->  Relay GND                   *
// *        D5      ->  Slit LED                    *
// *        D3      ->  Cal Relay IN1               *
// *        D4      ->  Flat Relay IN2              *
// *  - - - - - - - - - - - - - - - - - - - - - - - *
// *  3)  Optional Pinout                           *
// *      Arduino   ->  Device Pin                  *
// *      -------       -----------------           *
// *        D2          Hall Switch indicator LED   *
// **************************************************/

///**************************************************
// *                  Program Flow                  *
// **************************************************
// *  - Start by creating the stepper object        *
// *  - Initialize variables and run setup()        *
// *  - Read the current Hall switch status         *
// *  - If switch not triggered then HOME the motor *
// *  - Wait for incomming serial command character *
// *  - Move either IN to 0 or OUT to maxSteps      *
// *  - Mxxxx moves to the specified step ('-xxxx'  *
// *    means drive to the inward step relative to  *
// *    the 0 or homed position)                    *
// *  - If command is '0'(zero) then show status    *
// *  - If command is '?' then display command list *
// **************************************************/ 

///**************************************************
// *            User Defined Variables              *
// **************************************************/
const int switchLEDPin        = 2;                          // remote hall switch indicator LED (optional)
const int FlatRelayPin        = 3;                          // Flat lamp relay pin
const int CalRelayPin         = 4;                          // Cal lamp relay pin
const int SlitLEDPin          = 5;                          // LED to illuminate the slit
const int hallSwitchPin       = 7;                          // hall sensor pin
const int motorPinIN1         = 8;                          // IN-1 pins on UL2003 board
const int motorPinIN2         = 9;                          // IN-2 pins on UL2003 board
const int motorPinIN3         = 10;                         // IN-3 pins on UL2003 board
const int motorPinIN4         = 11;                         // IN-3 pins on UL2003 board
const int maxSteps            = -16000; //16384;            // abs maximum steps from homed (0) to fully inserted

int speedToRun                = 1000;                       // speed to run <= 2000 steps/sec
int testDelay                 = 3000;                       // delay in seconds while doing a lamp test
bool boolLocalCommands        = true;                       // flag to display local verbose replies
bool autoHome                 = false;                      // flag for autohome on start
///**************************************************
// *        END of User Defined Variables           *
// **************************************************/

// **************************************************
// *            Include Stepper Object              *
// **************************************************/
#include <Stepper.h>

///**************************************************
// *      Initialize Non-User Defined Variables     *
// *              DO NOT NODIFY THESE               *
// **************************************************/
int stepCount = 0;                                          // number of steps the motor has taken
const float STEPS_PER_REV     = 32;                         // motor steps ignoring the gearing
const float GEAR_RED          = 64;                         // approximate reduction of 64:1
const float STEPS_PER_REV_OUT = STEPS_PER_REV * GEAR_RED;   // includes reduction
int hallSwitchState           = 0;                          // holds the current switch state
int currentStep               = 0;                          // step counter, same as stepper.currentPosition()
int deltaSteps                = 0;                          // steps to move if not all IN or all OUT
bool bolHomeFound             = 0;                          // used to prevent continuious homming
String inputString            = "";                         // command string created from serial input
bool stringComplete           = false;                      // whether the string is complete                                     
String arrCommand[2];                                       // array holding command segments
const String helpCommands = " A->toggle AutoHome, , L->toggel Local commands w/ECHO,\n I->full inward O->full outward, Mxxxx->Move To xxxx,\n Rxxxx->Change speed to xxxx,\n F->Flat lamp ON, 5->Flat lamp OFF, C->Cal lamp ON,\n 6->Cal lamp OFF, S->Slit LED ON, 7->Slit LED OFF,\n 0->Step Status, T->Test all lamps, ?->this help";
// step pins are energized in this patterns for forward stepping 1-3-2-4
Stepper stepper(STEPS_PER_REV,8,10,9,11);                   // order is to be blue-yellow-pink-orange

int checkSwitchState(){
  // check the current state of the hall switch and return it as 0-not triggered or 1-triggered
  hallSwitchState = digitalRead(hallSwitchPin);
  if (hallSwitchState = 0){           // not triggered
    bolHomeFound = false;
    digitalWrite(switchLEDPin, LOW);  // turn off remote hall switch LED if installed
    return 0;
  }
  else {                              // triggered
    bolHomeFound = true;
    digitalWrite(switchLEDPin, HIGH); // turn on remote hall switch LED if installed
    return 1;
  }
}

void homeMotor(){
  // first check current hall switch state and if it is not ON (HOMED)
  // then drive motor outwards until hall switch triggers (HOMED)
  stepper.setSpeed(speedToRun);
  hallSwitchState = digitalRead(hallSwitchPin);
  if (hallSwitchState == 0){
    // motor is HOME so don't do anything but zero the step counter
    currentStep = 0;
    bolHomeFound = true;
    digitalWrite(switchLEDPin, HIGH);
    Serial.println("Motor is already homed!");
    return;
  }
  else {
     // motor is not at home so drive it there slowly with a recheck
     // by driving inward for XX steps and then back outward until
     // hall switch triggers
     while (digitalRead(hallSwitchPin) != 0){
       // drive outward and recheck
       stepper.step(50);
       checkSwitchState();
     }
      // now reset the counter
      stepCount = 0;  // zero the counter once homed 
      currentStep = 0;
      if (boolLocalCommands == true){
        Serial.println("Motor stepCount is now " + String(stepCount));
      }
      bolHomeFound = true;  
      digitalWrite(switchLEDPin, HIGH);  
   }
}

void toggleAutoHome(){
  if (autoHome == true){
    autoHome = false;
  }
  else{
    autoHome = true;
  }
}
void driveIN(int targetStep){ // ex. dSteps = -200 then drive in 200 steps
  // Drive inward to targetStep not to exceed maxSteps
  if (boolLocalCommands == true){
    Serial.println("speedToRun = " + String(speedToRun));
    Serial.println("Step currently at " + String(currentStep));
  }
  stepper.setSpeed(speedToRun);
  if (boolLocalCommands == true){
    Serial.println("Current step: " + String(currentStep) + " Driving IN to " + String(targetStep));
  }
  while (currentStep > targetStep){
    stepper.step(-10);  // remember that negative step values drive inward
    currentStep-= 10;
    if (boolLocalCommands == true){
     Serial.println("currentStep: " + String(currentStep) + " going to " + targetStep);
    }
  }
}

void driveOUT(int targetStep){    // ex. targetStep = -300 will drive out if currentStep is <= 0
  // Drive out to targetStep or until hall switch trips
  if (boolLocalCommands == true){
    Serial.println("speedToRun = " + String(speedToRun));
    Serial.println("currentStep = " + String(currentStep));
  }
  stepper.setSpeed(speedToRun);
  if (boolLocalCommands == true){
    Serial.println("Moving OUT to " + String(targetStep));
  }
  while (currentStep < targetStep){ 
    stepper.step(10);   // remember that positive steps drive outward
    currentStep+=10;
    if (boolLocalCommands == true){
      Serial.println("currentStep: " + String(currentStep) + " going to " + String(targetStep));
    }
  }
}

void runTo(int targetStep){
  // move motor to the desired step passed in provided we don't exceed maxSteps and not past HOME (0)
  if (targetStep != currentStep){   // otherwise just do nothing
    if (boolLocalCommands == true){
      Serial.println("Driving to " + String(targetStep) + " at speed " + String(speedToRun));
    }
    if (targetStep < currentStep){ // meaning we want to insert
      // Run in to targetStep
      if (boolLocalCommands == true){
        Serial.println("Driving IN from " + String(currentStep) + " to " + String(targetStep));
      }
      driveIN(targetStep);
    }
    else {
      // Run out to targetStep
      if (boolLocalCommands == true){
        Serial.println("Driving OUT from " + String(currentStep) + " to " + String(targetStep));
      }
      driveOUT(targetStep);
    }
  }
}

void resetCurrentStep(){
  // reset the currentStep to 0
  // perform HOME again
  bolHomeFound = false;
  homeMotor();
  if (boolLocalCommands == true){
    Serial.println("Position reset to 0 after homeing");
    Serial.println("currentStep = " +String(currentStep));
  }
}

void doCommandEvaluation(){
  // evaluate the incomming command and if it's length is > 1 then split it out and assign to arrCommand
  if (boolLocalCommands == true){
    Serial.println("inputString: " + inputString);
  }
  // Move to XXXX
  if ((inputString.startsWith("M")) || (inputString.startsWith("m"))){
   // split it out
    arrCommand[0] = "M";
    arrCommand[1] = inputString.substring(1).toInt();
    if (boolLocalCommands ==true){
      Serial.println("arrCommand[0]= " + arrCommand[0] + ", arrCommand[1]= " + arrCommand[1]);
    }
  }
  // Speed to RUN
  else if ((inputString.startsWith("R")) || (inputString.startsWith("r"))){
    arrCommand[0] = "R";
    arrCommand[1] = inputString.substring(1).toInt();
    if (boolLocalCommands ==true){
      Serial.println("arrCommand[0]= " + arrCommand[0] + ", arrCommand[1]= " + arrCommand[1]);
    }
  }
  else{
    // not an M or an R so just populate the arrCommand[0] with entire string
    arrCommand[0] = inputString;
    arrCommand[1] = "";
  }
  // now evaluate the action
  if (boolLocalCommands == true){
    Serial.println("arrCommand[0]: " + arrCommand[0] + ", arrCommand[1]: " + arrCommand[1]);
  }
  doAction();
  inputString = "";
}

int getStep(){
  return currentStep;
}

void getStatus(){             // currently not an active command
  String where = "";
  String theSwitch = "";
  String thePosition = "";
  String homeTriggered = "";
  // show the current status information
  if (boolLocalCommands == true){
    where = "YES";
  }
  else{
    where = "NO";
  }
  if (hallSwitchState = 1){
    theSwitch = "Homed";
  }
  else{
    theSwitch = "Not Homed";
  }
  if (currentStep == 0){
    // at home
    thePosition = "0, At Home";
  }
  else{
    thePosition = String(currentStep);
  }
  if (digitalRead(hallSwitchPin) == 0){
    // triggered
    homeTriggered = "YES";
  }
  else{
    homeTriggered = "NO";
  }
  if (boolLocalCommands ==true){
    Serial.println("=============== INJECTOR STATUS =================");
    Serial.println("   AutoHome:\t\t" + String(autoHome));
    Serial.println("   Speed:\t\t" + String(speedToRun));
    Serial.println("   Current step:\t" + thePosition);
    Serial.println("   Maximum step:\t" + String(maxSteps));
    Serial.println("   Local Commands:\t" + where);
    Serial.println("   Hall Switch State:\t" + theSwitch);
    Serial.println("   Hall Triggered Now:\t" + homeTriggered);
    Serial.println("================= End of STATUS =================");
  }
}

void doAction(){
  // decide what command to run
  ///**************************************************
  // *            Serial Command Protocol             *
  // **************************************************
  // *  A = toggle AutoHome feature                   *
  // *  H = home the injector                         *
  // *  L = toggle LOCAL commands for serial ECHO     *
  // *  I = drive inward, CW from above motor shaft   *
  // *  O = drive outward, CCW from above motor shaft *
  // *  M = move the steps value sent in (+/-)xxxxx   *
  // *  C = cal lamp relay ON                         *
  // *  5 = cal lamp relay OFF                        *
  // *  F = flat lamp relay ON                        *
  // *  6 = flat lamp relay OFF                       *
  // *  S = slit lamp LED ON                          *
  // *  7 = slit lamp LED OFF                         *
  // *  R = change speed to RUN                       *
  // *  T = test all three lamps                      *
  // *  Z = reset the zero point w/ homing            *
  // *  0 = (zero) get current step                   *
  // *  ? = brief help on commands                    *
  // *************************************************/

  // Help commands
  // Toggle the AutoHome feature
  if ((arrCommand[0] == "A") || (arrCommand[0] == "a")){
    toggleAutoHome();
    Serial.println("AutoHome toggled");
  }
  
  if (arrCommand[0] == "?"){
    if (boolLocalCommands == true){
    // display help commands
      showHelp();
    }
    return;
  }
  // Home injector
  else if ((arrCommand[0] == "H") || (arrCommand[0] == "h")){
    // home the system, just use the resetCurrentStep function
    homeMotor();
    Serial.println("Homed");    // ==> Reply through serial
    return;
  }
  // Toggle LOCAL commands
  else if ((arrCommand[0] == "L") || (arrCommand[0] == "l")){
    if (boolLocalCommands == true){
      boolLocalCommands = false;
      Serial.println("Local OFF");    // ==> Reply through serial
    }
    else{
      boolLocalCommands = true;
      Serial.println("Local ON");    // ==> Reply through serial
    }
    return;
  }
  // Send out currentStep
  else if (arrCommand[0] == "0"){   // && (boolLocalCommands == true){ //zero
    //Serial.println("Getting the step in Arduino");
    Serial.println("currentStep: " + String(currentStep));
    //getStatus();
    return;
  }
  // Move to XXXX
  else if ((arrCommand[0] == "M") || (arrCommand[0] == "m")){
    // move to the requested step
   int targetStep = arrCommand[1].toInt();
      runTo(targetStep);
        Serial.println("Step = " + String(targetStep));    // ==> Reply through serial
      return;
    }
    // Zero the step counter
  else if ((arrCommand[0] == "Z") || (arrCommand[0] == "z")){
    // reset the counter to zero
    resetCurrentStep();
    Serial.println("Step counter zeroed");
    return;
  }
  // Speed to RUN
  else if ((arrCommand[0] == "R") || (arrCommand[0] == "r")){
    // set the speedToRun variable to the value of arrCommand[1]
    if ((arrCommand[1].toInt() >= -16000) && (arrCommand[1].toInt() >= 250)){
      // We are in reasonable range
      speedToRun = arrCommand[1].toInt();
        Serial.println("Speed = " + String(speedToRun));
    }
    return;
  }
  // Insert injector
  else if ((arrCommand[0] == "I") || (arrCommand[0] == "i")){
    // drive it in to maxSteps
    if (boolLocalCommands == true){
      Serial.println("Moving inward " + String(abs(deltaSteps)) + " steps to fully inserted");
    }
    driveIN(maxSteps);    // might need to uncomment
    Serial.println("Fully inserted");
    return;
  }
  // Remove injector
  else if ((arrCommand[0] == "O") || (arrCommand[0] == "o")){
    // drive it out
    if (boolLocalCommands == true){
      Serial.println("Moving out to ZERO");
    }
    homeMotor();
    Serial.println("Injector removed");
    return;
  }
  // CAL lamp ON
  else if ((arrCommand[0] == "C") || (arrCommand[0] == "c")){
    // turn ON the cal lamp relay set it LOW
    digitalWrite(CalRelayPin, LOW);
    Serial.println("Cal lamp ON");    // ==> Reply through serial
    return;
  }
  // CAL lamp OFF
  else if (arrCommand[0] == "5"){
    // turn OFF the cal lamp relay set it HIGH
    digitalWrite(CalRelayPin, HIGH);
    Serial.println("Cal lamp OFF");    // ==> Reply through serial
    return;
  }
  // FLAT lamp ON
  else if ((arrCommand[0] == "F") || (arrCommand[0] == "f")){
    // turn ON the flat lamp relay set it LOW
    digitalWrite(FlatRelayPin, LOW);
    Serial.println("Flat lamp ON");    // ==> Reply through serial
    return;
  }
  // FLAT lamp OFF
  else if (arrCommand[0] == "6"){
    // turn OFF the flat lamp relay set it HIGH
    digitalWrite(FlatRelayPin, HIGH);
    Serial.println("Flat lamp OFF");    // ==> Reply through serial
    return;
  }
  // SLIT lamp ON
  else if ((arrCommand[0] == "S") || (arrCommand[0] == "s")){
    // turn on the slit LED set it HIGH
    digitalWrite(SlitLEDPin, HIGH);
    Serial.println("Slit LED ON");    // ==> Reply through serial
    return;
  }
  // SLIT lamp OFF
  else if (arrCommand[0] == "7"){
    // turn OFF the slit LED set it LOW
    digitalWrite(SlitLEDPin, LOW);
    Serial.println("Slit LED OFF");    // ==> Reply through serial
    return;
  }
  // Test all lamps
  else if ((arrCommand[0] == "T") || (arrCommand[0] == "t")){
    // test all lamps for 5 seconds
    if (boolLocalCommands == true){
      Serial.println("Testing all lamps for " + String(testDelay/1000) + " seconds");
    }

    digitalWrite(CalRelayPin, LOW);
    delay(100);
    digitalWrite(SlitLEDPin, HIGH);
    delay(100);
    digitalWrite(FlatRelayPin, LOW);
    delay(testDelay);
    digitalWrite(SlitLEDPin, LOW);
    digitalWrite(CalRelayPin, HIGH);
    digitalWrite(FlatRelayPin, HIGH);
    if (boolLocalCommands == true){
      Serial.println("All lamps now OFF");
    }
    return;
  }
}

void showHelp(){
  if (boolLocalCommands ==true){
    // display the help commands
    Serial.println("======================= COMMANDS =========================");
    Serial.println(helpCommands);
    Serial.println("(Local command mode ON by default, AutoHome OFF by default)");
    Serial.println("===================== END OF COMMANDS ====================");
  }
}

void getInput(){
  while (Serial.available()) {
    String strCommand = "";
    // get the new bytes:
    strCommand = Serial.readString();
    Serial.println("strCommand: " + strCommand);
    inputString = strCommand;
    stringComplete = true;
    // evaluate what the command is
    doCommandEvaluation();
  }
}

// run setup()
void setup() {
  stepper.setSpeed(speedToRun);
  pinMode(switchLEDPin, OUTPUT);
  pinMode(hallSwitchPin, INPUT_PULLUP);
  pinMode(FlatRelayPin, OUTPUT);
  pinMode(CalRelayPin, OUTPUT);
  pinMode(SlitLEDPin, OUTPUT);
  digitalWrite(FlatRelayPin, HIGH);
  digitalWrite(CalRelayPin, HIGH);
  digitalWrite(SlitLEDPin, LOW);
  Serial.begin(19200);
  Serial.flush();
  if (boolLocalCommands == true){
    showHelp();
  }
}

void loop() {
  // read the hall switch state and perform a HOME if necessary
  hallSwitchState = digitalRead(hallSwitchPin);
  // decide what to do about homing
  if ((bolHomeFound == false) && (autoHome == true)){
    switch (hallSwitchState){
      case 0:   // already at home so just wait for a command to come in on the Serial port
        digitalWrite(switchLEDPin, HIGH);
        if (boolLocalCommands == true){
          Serial.println("Switch is now " + String(hallSwitchState) + " which is ON, HOME NOT needed!");
        }
        bolHomeFound = true;
        currentStep = 0;
        // no need to home
        break;
      case 1:
        digitalWrite(switchLEDPin, LOW);
        if (boolLocalCommands == true){
          Serial.println("Switch is now " + String(hallSwitchState) + " which is OFF, HOMING!");
        }
        bolHomeFound = false;
        // need to home
        homeMotor();  // home the motor
        currentStep = 0;
        if (boolLocalCommands == true){
          Serial.println("Homing complete, currentStep set to ZERO");
        }
        break;
    }
  }
    while (Serial.available()) {
    String strCommand = "";
    // get the new bytes:
    strCommand = Serial.readStringUntil('\n');
    inputString = strCommand;
    stringComplete = true;
    // evaluate what the command is
    doCommandEvaluation();
  }
  delay(500);
  deltaSteps = (maxSteps - currentStep);
}
