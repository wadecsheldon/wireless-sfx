
void setup()
{
  Serial.begin(57600);
  pinMode(2, INPUT);
}

void loop()
{
  if(digitalRead(2) == HIGH)
  {
    Serial.write(127);
    while(digitalRead(2) == HIGH)
    {
      delay(50);
    }
  }
}
