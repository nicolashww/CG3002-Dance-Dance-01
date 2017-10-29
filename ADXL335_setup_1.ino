const int xpin1 = A0;
const int ypin1 = A1;
const int zpin1 = A2;

const int xpin2 = A3;
const int ypin2 = A4;
const int zpin2 = A5;

//const int xpin3 = A6;
//const int ypin3 = A7;
//const int zpin3 = A8;

//const int xpin4 = A9;
//const int ypin4 = A10;
//const int zpin4 = A11;

void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
}

void loop() {
  // put your main code here, to run repeatedly:
  int x1 = analogRead(xpin1);
  delay(1);
  int y1 = analogRead(ypin1);
  delay(1);
  int z1 = analogRead(zpin1);
  delay(1);

  int x2 = analogRead(xpin2);
  delay(1);
  int y2 = analogRead(ypin2);
  delay(1);
  int z2 = analogRead(zpin2);
  delay(1);

  //int x3 = analogRead(xpin3);
  //delay(1);
  //int y3 = analogRead(ypin3);
  //delay(1);
 // int z3 = analogRead(zpin3);
  //delay(1);

 // int x4 = analogRead(xpin4);
  //delay(1);
  //int y4 = analogRead(ypin4);
  //delay(1);
  //int z4 = analogRead(zpin4);
  

  
  Serial.print(x1); Serial.print("\t"); Serial.print(y1); Serial.print("\t"); Serial.print(z1); Serial.print("\t");

  Serial.print(x2); Serial.print("\t"); Serial.print(y2); Serial.print("\t"); Serial.print(z2); Serial.print("\n");

  //Serial.print(x3); Serial.print("\t"); Serial.print(y3); Serial.print("\t"); Serial.print(z3); Serial.print("\t");

  //Serial.print(x4); Serial.print("\t"); Serial.print(y4); Serial.print("\t"); Serial.print(z4); Serial.print("\n");

  
}
