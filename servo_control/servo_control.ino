#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

const int buttonPin = 2;
int pos = 0;    // variable to store the servo position
int GCNT = 0;
int cnt = 0;
int GBTState = HIGH;
void setup() {
  myservo.attach(11);  // attaches the servo on pin 9 to the servo object
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600); // 시리얼 통신 시작 (디버깅용)
}

void loop() {
  GBTState = digitalRead(buttonPin);
  if (GBTState == LOW) {
    // turn LED on:
    GCNT += 1;
    if (GCNT >= 2)
    {
      GCNT = 0;
    }
    delay(1000);
  }
  if (GCNT == 1){
    for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
      // in steps of 1 degree
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(1);                       // waits 15 ms for the servo to reach the position
    }
    for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(1);                       // waits 15 ms for the servo to reach the position
    }
    cnt += 1;
    if (cnt == 10)
    {
      Serial.println("1");
      cnt = 0;    
    }
  }
  else if (GCNT == 0)
  {
    pos = 0;
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(1);  
  }
  delay(200); 
}
