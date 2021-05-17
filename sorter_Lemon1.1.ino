#include <Servo.h>

Servo gate;
Servo sorter;// create servo object to control a servo
int Lemon;

int a = 90;    // variable to store the servo position
int b = 90;

void setup() {
  gate.attach(6);  // attaches the servo on pin 9 to the servo object
  sorter.attach(5);

  //first condition of gates and sorter
  gate.write(90); 
  delay(5);
  sorter.write(90);
  delay(5);
 
 //serial
Serial.begin(115200);
 Serial.setTimeout(1); // put your setup code here, to run once:

}

void loop() {
 while (!Serial.available());
 Lemon = Serial.readString().toInt();
 Serial.print(Lemon);

if (Lemon == 1) {
  sorting();
  gating();
  Serial.println("matang");
  delay(5);
}
else if (Lemon == 2) { 
  sorting2();
  gating();
   Serial.println("tidak matang");
  delay(5);
}
 gate.write(90); 
  delay(5);
  sorter.write(90);
  delay(5);

}
void gating() {
  for (a = 90; a <= 45; a += 1) { // goes from 0 degrees to 45 degrees
    // in step   \=oooooooooooos of 1 degree
    gate.write(a);              // tell servo to go to position in variable 'pos'
    delay(20);
   }
    }

void sorting() {
  for (b = 90; b >= 45; b -= 2) { // goes from 90 degrees to 45 degrees
    sorter.write(b);
    delay(10);
    
  }
}

void sorting2() {
  for (b = 90; b <= 135; b += 2) { // goes from 90 degrees to 135 degrees
    sorter.write(b);
    delay(10);
    
  }
}
