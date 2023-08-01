#include <SPI.h>

void setup() {
  Serial.begin(9600);
  pinMode(MISO, OUTPUT);
  SPCR |= _BV(SPE);
  SPI.attachInterrupt();
}

byte odebrane_dane = 0;

ISR (SPI_STC_vect) {
  byte odebrane_dane = SPDR;
  Serial.print("odebralem: ");
  Serial.println(odebrane_dane);

  //dane które chcemy wysłać przypisujemy do tej zmiennej 
  SPDR = 10;
}

void loop () {

}



