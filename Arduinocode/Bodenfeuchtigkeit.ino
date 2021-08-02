

void setup() {
  // put your setup code here, to run once:
  pinMode(A0, INPUT);             // A0 als Eingang definieren
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  Serial.begin(9600);              // Serielle Kommunikation mit 9600 Baud
  delay(500);

}



void loop() {
  int sensorValue1 = analogRead(A0);
  int sensorValue2 = analogRead(A1);
  int sensorValue3 = analogRead(A2);
  int sensorValue4 = analogRead(A3);
  int sensorValue5 = analogRead(A4);
  // put your main code here, to run repeatedly:
  //Serial.print("[");
  Serial.print(sensorValue1);
  Serial.print(",");
  Serial.print(sensorValue2);
  Serial.print(",");
  Serial.print(sensorValue3);
  Serial.print(",");
  Serial.print(sensorValue4);
  Serial.print(",");
  Serial.print(sensorValue5);
  //Serial.println("]");
  //Serial.print(",");
  //Serial.println();
  Serial.print("\r\n");
  delay(1000);

  //Serial.print(temperatur_data);
  

}
