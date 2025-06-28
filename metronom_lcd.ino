#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2); // LCD adresi, sütun, satır

int buzzerPin = 8;
int bpm = 60;
int increment = 4;
int period = 16;
int counter = 0;
bool isRunning = false;

unsigned long previousMillis = 0;
unsigned long interval = 1000;

void setup() {
  Serial.begin(9600);
  pinMode(buzzerPin, OUTPUT);

  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("   BPmO HAZIR");
  lcd.setCursor(0, 1);
  lcd.print("   BPM: --");
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    data.trim();

    if (data == "START") {
      isRunning = true;
      counter = 0;
      previousMillis = millis();
      interval = 60000 / bpm;
      Serial.println("Started");
    }
    else if (data == "STOP") {
      isRunning = false;
      Serial.println("Stopped");
      lcd.setCursor(0, 1);
      lcd.print("BPM: --        "); // Eski yazıyı silmek için boşluklar
    }
    else if (data == "EXIT") {
      isRunning = false;
      Serial.println("Exiting");
    }
    else {
      int sep1 = data.indexOf(',');
      int sep2 = data.indexOf(',', sep1 + 1);
      if (sep1 > 0 && sep2 > sep1) {
        bpm = data.substring(0, sep1).toInt();
        increment = data.substring(sep1 + 1, sep2).toInt();
        period = data.substring(sep2 + 1).toInt();
        interval = 60000 / bpm;
        counter = 0;
        Serial.println("Params set");
      }
    }
  }

  if (isRunning) {
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;

      tone(buzzerPin, 1000, 100);
      counter++;

      Serial.print("BPM:");
      Serial.println(bpm);

      // LCD'ye mevcut BPM'i yazdır
      lcd.setCursor(0, 1);
      lcd.print("BPM: ");
      lcd.print(bpm);
      lcd.print("    "); // Önceki sayıdan kalan karakterleri temizlemek için boşluk

      if (counter % period == 0) {
        bpm += increment;
        interval = 60000 / bpm;
      }
    }
  }
}
