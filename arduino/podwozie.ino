void setup() {
  Serial.begin(9600);
}

void loop() {
  static unsigned long last_time = 0;
  unsigned long current_time = millis();
  unsigned long interval = 100; 

  if (current_time - last_time >= interval) {
    while (!Serial.available()) {}
    String data_received = Serial.readStringUntil('\n');

    Serial.println(data_received);

    last_time = current_time;
  }
}


