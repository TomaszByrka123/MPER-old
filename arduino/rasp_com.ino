#include <SPI.h>

void setup() {
  Serial.begin(9600);
  pinMode(MISO, OUTPUT);
  SPCR |= _BV(SPE);
  SPI.attachInterrupt();
}

ISR (SPI_STC_vect) {
  byte c = SPDR;
  Serial.write("wyslalem");
  SPDR = c + 10;
}

void loop () {
  static unsigned long previousMillis = 0;
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= 1000) {
    previousMillis = currentMillis;
    SPDR = random(101); // Wysyłanie losowej liczby od 0 do 100
  }
}
