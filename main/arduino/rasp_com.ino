 #include "CytronMotorDriver.h"
 #include <SPI.h>


// Configure the motor driver.
CytronMD motor1(PWM_DIR, A1, A2);  // PWM 1 = Pin 3, DIR 1 = Pin 4.
CytronMD motor2(PWM_DIR, 3, 4); // PWM 2 = Pin 9, DIR 2 = Pin 10.


// The setup routine runs once when you press reset.
void setup() {
  Serial.begin(9600);
  pinMode(MISO, OUTPUT);
  SPCR |= _BV(SPE);
  SPI.attachInterrupt();
}

byte odebrane_dane = 0;
ISR (SPI_STC_vect) {
  byte odebrane_dane = SPDR;
  if (odebrane_dane == 1) {
      motor1.setSpeed(128);   // Motor 1 runs forward at 50% speed.
      motor2.setSpeed(128);  // Motor 2 runs backward at 50% speed.
      delay(200);
  } 
  else if (odebrane_dane == 2) {
      motor1.setSpeed(-128);   // Motor 1 runs forward at 50% speed.
      motor2.setSpeed(-128);  // Motor 2 runs backward at 50% speed.
      delay(200);
  } 
  else if (odebrane_dane == 3) {
      motor1.setSpeed(128);   // Motor 1 runs forward at 50% speed.
      motor2.setSpeed(-128);  // Motor 2 runs backward at 50% speed.
      delay(200);  
  }
  else if (odebrane_dane == 4) {
      motor1.setSpeed(-128);   // Motor 1 runs forward at 50% speed.
      motor2.setSpeed(128);  // Motor 2 runs backward at 50% speed.
      delay(200);
  }

  //dane które chcemy wysłać przypisujemy do tej zmiennej 
  SPDR = 10;
}



// The loop routine runs over and over again forever.
void loop() {
  motor1.setSpeed(128);   // Motor 1 runs forward at 50% speed.
  motor2.setSpeed(-128);  // Motor 2 runs backward at 50% speed.
  delay(1000);
  
  motor1.setSpeed(255);   // Motor 1 runs forward at full speed.
  motor2.setSpeed(-255);  // Motor 2 runs backward at full speed.
  delay(1000);

  motor1.setSpeed(0);     // Motor 1 stops.
  motor2.setSpeed(0);     // Motor 2 stops.
  delay(1000);

  motor1.setSpeed(-128);  // Motor 1 runs backward at 50% speed.
  motor2.setSpeed(128);   // Motor 2 runs forward at 50% speed.
  delay(1000);
  
  motor1.setSpeed(-255);  // Motor 1 runs backward at full speed.
  motor2.setSpeed(255);   // Motor 2 runs forward at full speed.
  delay(1000);

  motor1.setSpeed(0);     // Motor 1 stops.
  motor2.setSpeed(0);     // Motor 2 stops.
  delay(1000);
}
