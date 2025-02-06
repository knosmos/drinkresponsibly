#include <AccelStepper.h>

#define STEP_CNT 200

// Define some steppers and the pins the will use
AccelStepper stepper1(AccelStepper::FULL2WIRE, 3, 2); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
AccelStepper stepper2(AccelStepper::FULL2WIRE, 5, 4);
 
void setup()
{  
    stepper1.setMaxSpeed(10 * 200.0);
    stepper1.setAcceleration(1000.0);
    stepper1.moveTo(200 * 3);
    stepper2.setMaxSpeed(10 * 200.0);
    stepper2.setAcceleration(1000.0);
    stepper2.moveTo(200 * 3);
}
 
void loop()
{
    // Change direction at the limits
    if (stepper1.distanceToGo() == 0)
        stepper1.moveTo(-stepper1.currentPosition());
    if (stepper2.distanceToGo() == 0)
        stepper2.moveTo(-stepper2.currentPosition());
    stepper1.run();
    stepper2.run();
}
