#include <AccelStepper.h>

#define STEP_CNT 200

// Define some steppers and the pins the will use
AccelStepper stepper1(AccelStepper::DRIVER, 3, 2); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
AccelStepper stepper2(AccelStepper::DRIVER, 5, 4);

// Pulley diameter and steps per rotation
const float stepsPerRotation = 200.0;
const float cmPerStep = (4.0) / stepsPerRotation;

int s1 = 5000;
int s2 = 5000;

void setup()
{  
    stepper1.setMaxSpeed(5000);
    stepper2.setMaxSpeed(5000);
    stepper1.disableOutputs();
    stepper2.disableOutputs();
    Serial.begin(115200);
}

void loop()
{
  if(Serial.available()>0){
    int targetX, targetY;
    uint32_t receivedData = (Serial.parseInt());
    Serial.read();
    targetX = receivedData % 1000;
    targetY = receivedData / 1000;
          
    // Convert mm to steps
    int stepsX = targetX / cmPerStep;
    int stepsY = targetY / cmPerStep;
          
    // CoreXY transformation
    int p1 = stepsX + stepsY;
    int p2 = stepsX - stepsY;
    
    Serial.println(p1);
    Serial.println(p2);
    stepper1.enableOutputs();
    stepper2.enableOutputs();
    stepper1.moveTo(p1);
    stepper2.moveTo(p2);
    s1 = (stepper1.distanceToGo() > 0) ? 1000 : -1000;
    s2 = (stepper2.distanceToGo() > 0) ? 1000 : -1000;
  }
  if (-20 < stepper1.distanceToGo() && stepper1.distanceToGo() < 20) {
    //stepper1.disableOutputs();
    //Serial.println("stepper 1 disabled!");
    stepper1.setSpeed(0);
  }
  else {
    stepper1.setSpeed(s1);
  }
  if (-20 < stepper2.distanceToGo() && stepper2.distanceToGo() < 20) {
    //stepper2.disableOutputs();
    //Serial.println("stepper 2 disabled!");
    stepper2.setSpeed(0);
  }
  else {
    stepper2.setSpeed(s2);
  }
  stepper1.runSpeed();
  stepper2.runSpeed();
}