// on Arduino
int sensorPin = A0;

int sensorValue = 0;

void setup(){
  Serial.begin(9600);
}

void loop(){
  int i = 1;
  sensorValue = analogRead(sensorPin);
  Serial.println(sensorValue);
  delay(5000); // sleep for 5 seconds
}
