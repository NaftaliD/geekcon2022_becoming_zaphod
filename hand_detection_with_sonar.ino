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
}

void loop() {
  if (calc_dis() < dt)
  {
    servo.write(180);
  }
  else
  {
    servo.write(0);
  }
}

int calc_dis()
{
  int duration,distance;
  digitalWrite(trig, HIGH);
  delay(dt);
  digitalWrite(trig, LOW);
  duration=pulseIn(echo, HIGH);
  distance = (duration / 2) / 29.1;
  
  return distance;
}