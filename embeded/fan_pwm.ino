#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT22
int PWM = 3;
float sensorVal;
int PWMVal;

DHT dht(DHTPIN, DHTTYPE);
long datafromUser=20;

void setup() {
  // put your setup code here, to run once:
  dht.begin(); // initialize the sensor
  pinMode(PWM, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if(Serial.available() > 0) {
    long value = 0;
    value = Serial.parseInt();
    if(value > 0)
    {
      datafromUser = value;
    }
    //Serial.print(String(datafromUser));
  }
  float tempC = dht.readTemperature();
  tempC = tempC / 256 * 10;
  Serial.println(sensorVal);
  delay(1000);
  sensorVal = tempC;
  if(sensorVal > datafromUser){
    //Serial.println("pwm HIGH" );
    digitalWrite(PWM, HIGH);
  }else{
    digitalWrite(PWM, LOW);
  }
}
