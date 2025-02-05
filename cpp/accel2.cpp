#include <AccelStepper.h>

#define STEP_CNT 200

// Define some steppers and the pins the will use
AccelStepper stepper1(AccelStepper::DRIVER, 3, 2); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
AccelStepper stepper2(AccelStepper::DRIVER, 5, 4);

int s1 = 1000;
int s2 = 1000;

void setup()
{  
    stepper1.setMaxSpeed(10 * 300.0);
    //stepper1.setAcceleration(1000.0);
    //stepper1.setSpeed(s1);
    stepper1.moveTo(200 * 1);
    stepper1.setSpeed(s1);
    stepper2.setMaxSpeed(10 * 300.0);
    //stepper2.setAcceleration(1000.0);
    //stepper2.setSpeed(s2);
    stepper2.moveTo(200 * 1);
    stepper2.setSpeed(s2);
    Serial.begin(115200);
}

int ctr = 0;
void loop()
{
    ctr++;
    ctr %= 10000;
    // Change direction at the limits
    if (ctr == 0) {
        s1 *= -1;
        //stepper1.setSpeed(s1);
        stepper1.moveTo(-stepper1.currentPosition());
        s2 *= -1;
        //stepper2.setSpeed(s2);
        stepper2.moveTo(-stepper2.currentPosition());
        stepper2.setSpeed(s2);
    }
    if (ctr % 1000 == 0) {
      Serial.println(stepper1.distanceToGo());
    }
    stepper1.setSpeed(s1);
    stepper2.setSpeed(s2);
    stepper1.runSpeed();
    stepper2.runSpeed();
}