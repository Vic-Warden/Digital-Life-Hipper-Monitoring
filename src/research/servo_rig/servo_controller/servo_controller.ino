#include "Wire.h"
#include "Adafruit_PWMServoDriver.h"

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define USMIN  600
#define USMAX  2400
#define SERVO_FREQ 50

uint8_t servonum = 15;

void setup() {
  Serial.begin(9600);
  Serial.println("PCA9685ServoV1");

  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);

  delay(10);
}

void loop() {
  // Use a larger step size for faster movement
  for (uint16_t microsec = USMIN; microsec < USMAX; microsec += 10) {
    pwm.writeMicroseconds(servonum, microsec);
    delay(2);  // Optional: reduce delay further if needed
  }
  Serial.println("A");

  delay(300);

  for (uint16_t microsec = USMAX; microsec > USMIN; microsec -= 10) {
    pwm.writeMicroseconds(servonum, microsec);
    delay(2);  // Optional: reduce delay further if needed
  }
  Serial.println("B");

  delay(300);
}
