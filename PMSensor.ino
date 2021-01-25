#include "SdsDustSensor.h"
#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

int rxPin = 0;
int txPin = 1;
SdsDustSensor sdsSensor(rxPin, txPin);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  sdsSensor.begin();

}

void loop() {
  // put your main code here, to run repeatedly:
  PmResult pm = sdsSensor.readPm();
  if (pm.isOk()) {
    //Serial.print("PM 2.5: ");
    Serial.print(pm.pm25);
    Serial.print(",");
    //Serial.print(",PM 10: ");
    Serial.println(pm.pm10);
  } else {
    Serial.println("No Data");
  }

  delay(1000);
}
