#include<Servo.h>

// Vars
int trig = 8;
int echo = 9;
int dt   = 10;
Servo servo;

void setup() {
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  Serial.begin(9600);
  servo.attach(11);
  servo.write(0);
}

int is_locked = 0;
unsigned long lock_start = 0;

void loop() {
  Serial.println(millis() - lock_start);
  if (calc_dis() < dt) {
    is_locked = 1;
    servo.write(180);
    lock_start = millis();
  }
  else if (is_locked && (millis() - lock_start > 1000))  {
    is_locked = 0;
    servo.write(0);
  }
}

int calc_dis() {
  int duration,distance;
  digitalWrite(trig, HIGH);
  delay(dt);
  digitalWrite(trig, LOW);
  duration=pulseIn(echo, HIGH);
  distance = (duration / 2) / 29.1;
  
  return distance;
}
