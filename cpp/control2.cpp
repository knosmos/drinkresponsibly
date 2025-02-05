#define PI 3.1415926
#define DEG_TO_RAD 0.017453292519943295769236907684886
#define sgn(x) ((x) < 0 ? -1 : ((x) > 0 ? 1 : 0))

int DIRPIN1 =  2;
int STEPIN1 = 3;
int DIRPIN2  = 4;
int STEPIN2  = 5;

#define TOTAL_STEPS 200

void setup() {
  pinMode(DIRPIN1,OUTPUT);
  pinMode(STEPIN2,OUTPUT);
  pinMode(DIRPIN1,OUTPUT);
  pinMode(DIRPIN2,OUTPUT);
  Serial.begin(115200);
//  left(400);
//  up(400);
//  right(400);
//  down(400);
  // delay(1000);
  // angleDrive(300,0);

}


int drive = 0; 
int angle = 0; 
void loop() {

  if(Serial.available()>0){
      int receivedData = (Serial.parseInt());
      move_x(receivedData);
      Serial.read();
//    if (receivedData == 1){
//      up(200);
//    }
//    if (receivedData == 2){
//      down(200);
//    }
//    if (receivedData == 3){
//      left(200);
//    }
//    if (receivedData == 4){
//      right(200);
//    }
//    if (receivedData == 5){
//      v1(200);
//    }
//    if (receivedData == 6){
//      v2(200);
//    }
//    if (receivedData == 7){
//      v3(200);
//    }
//    if (receivedData == 8){
//      v4(200);
//    }
//    if (receivedData == 9){
//      while(true){
//        left(800);
//        up(800);
//        right(800);
//        down(800);
//        
//       }
//    }
//    else{
//      angle = receivedData;
//    }
//    receivedData = (Serial.read());
//
//    Serial.print(drive);
//    Serial.print(",");
//    Serial.println(angle);
  }
  // put your main code here, to run repeatedly:
}

float speed = 7; 
int timer = 1000/speed; 

void angleDrive(int cycles, int angle){
  motorMove(cycles/10, int(10*sin(DEG_TO_RAD*(angle+45))), int(10*cos(DEG_TO_RAD*(angle+45))));
}
// up(TOTAL_STEPS);//left
// right(TOTAL_STEPS);//right
// left(TOTAL_STEPS);//up
// down(TOTAL_STEPS);//down

int curr = 0;
void move_x(int pos) {
  int d = pos * 50 - curr;
  motorMove(abs(d), sgn(d)*1, sgn(d)*-1);
  curr = pos * 50;
}

void left(int cycles){
  motorMove(cycles, 1,1);
}
void down(int cycles){
  motorMove(cycles, 1,-1);
}
void right(int cycles){
  motorMove(cycles, -1,-1);
}
void up(int cycles){
  motorMove(cycles, -1,1);
}
void v1(int cycles){
  motorMove(cycles, 0,1);
}
void v2(int cycles){
  motorMove(cycles, 0,-1);
}
void v3(int cycles){
  motorMove(cycles, -1,0);
}
void v4(int cycles){
  motorMove(cycles, 1,0);
}


void motorMove(int cycles, int pos1, int pos2){
  if (pos1 >= 0)
    digitalWrite(DIRPIN1, HIGH);
  else{
    digitalWrite(DIRPIN1, LOW);
    pos1 = -pos1; 
  }
  if (pos2 >= 0)
    digitalWrite(DIRPIN2, HIGH);
  else{
    digitalWrite(DIRPIN2, LOW);
    pos2 = -pos2; 
  }

  for(int x = 0; x < cycles; x++)
  {
    for (int i = 0; i < pos1; i++){
      digitalWrite(STEPIN1, HIGH);
      delayMicroseconds(timer);
      digitalWrite(STEPIN1, LOW);
      delayMicroseconds(timer);
    }
    for (int j = 0; j < pos2; j++){
      digitalWrite(STEPIN2, HIGH);
      delayMicroseconds(timer);
      digitalWrite(STEPIN2, LOW);
      delayMicroseconds(timer);
    }
  }
}