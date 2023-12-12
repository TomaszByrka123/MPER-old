void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    
    int commaIndex = data.indexOf(',');
    if (commaIndex != -1) {
      String x_str = data.substring(0, commaIndex);
      int x = x_str.toInt();
      
      String y_str = data.substring(commaIndex + 1);
      int y = y_str.toInt();
      
      Drive(x, y);
    }
  }
}


void Drive(int x, int y)
{
  x *= 2.55;
  y *= 2.55;
  
  if(x > 0)
  {
    analogWrite(2, x);
    analogWrite(3, 0);
  }

  if(x < 0)
  {
    analogWrite(2, 0);
    analogWrite(3, x);
  }

   if(y > 0)
  {
    analogWrite(A2, y);
    analogWrite(A3, 0);
  }

  if(y < 0)
  {
    analogWrite(A2, 0);
    analogWrite(A3, y);
  }
  
}