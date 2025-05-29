#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define SENSOR_PIN 34

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {

  Serial.begin(115200);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Umidade do Solo");

}

void loop() {

  int leitura = analogRead(SENSOR_PIN);

  // Processo de definição entre 0% e 100%
  int umidade = map(leitura, 0, 4095, 100, 0);

  // Processo de exibição no monitor serial
  /*Serial.print("Leitura: ");
  Serial.print(leitura);
  Serial.print(" | Umidade: ");
  Serial.print(umidade);
  Serial.println("%");*/

  // Processo de exibição no display
  lcd.setCursor(0, 1);
  lcd.print("Umidade: ");
  lcd.print(umidade);
  lcd.print(" %   ");

  delay(1000);

}