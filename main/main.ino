#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
#define RED 3
#define GREEN 5
#define BLUE 2
#define trigPin 6
#define echoPin 7

MFRC522 mfrc522(SS_PIN, RST_PIN);  

bool reserved = false; 
String id = "";
String user_uid = "";
bool have_user_id = false;
float duration, distance;
bool debug = false;

void setup() {
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
  pinMode(RED, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);   // Initiate a serial communication
  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
  setColor(255, 0, false);
  restart();
  
}

void loop() {
  get_id();
  while (occupied()) {
    if (reserved) {
      // Set yellow
      while (! mfrc522.PICC_IsNewCardPresent() and occupied()){
        setColor(100, 0, true);
      }
      if ( ! mfrc522.PICC_ReadCardSerial()) {
        return;
      }
      if (!have_user_id) {
        get_user_id();
        have_user_id = true;
      }
      if (check_UID()) {
        if (debug) {
          Serial.print("correct UID");
        }
        while(occupied()){
          setColor(0, 255, false);
        }
        restart();
        return;
      }
      if (!check_UID()) {
        // Set red
        if (debug) {
          Serial.print("Incorrect UID");
        }
        while (occupied()) {
          setColor(0, 0, true);
        }
        restartReserved();
        return;
      }
    }
    if (!reserved){
      // Set LED blue
      Serial.println(0);
      if (debug) {
        Serial.print("Someone in stall not booked");
      }
      while(occupied()) {
        setColor(0, 255, false);
      }
      restart();
      return;
    }
  }
}

void get_user_id() {
  
  // Get UID as string variable
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     user_uid.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : " "));
     user_uid.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  user_uid.toUpperCase();
  // Substring used too exclude whitespace at the begining 
  user_uid = user_uid.substring(1);
  // Serial.println(user_uid);
}

bool check_UID() {
  if (user_uid == id) {
    return true;
  }
  else {
    return false;
    }
}

void get_id() {
  if (id != "") {
    reserved = true;
    setColor(0, 255, false);
  }
  while (Serial.available() > 0) 
  {
    id = Serial.readString();
  }
}

bool occupied() {
  // uses ultrasonic sensors to detect presence of vehicle
  digitalWrite(trigPin, LOW);
  delay(2);
  digitalWrite(trigPin, HIGH);
  delay(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  delay(500);
  distance = (duration / 2) * 0.0343;
  if (distance <= 20){
    return true;
  }
  else {
    return false;
  }
}

void resetRFIDReader() {
  // Reset the MFRC522 by toggling the RST pin
  digitalWrite(RST_PIN, LOW);  // Assuming SS_PIN is connected to the RST pin
  delay(100);  // Keep the pin low for a short duration (adjust as needed)
  digitalWrite(RST_PIN, HIGH);  // Release the RST pin by bringing it HIGH
  delay(100);  // Allow some time for the MFRC522 to initialize (adjust as needed)
}
void restart() {
  setColor(255, 0, false);
  Serial.println(1);
  reserved = false; 
  id = "";
  user_uid = "";
  have_user_id = false;
  resetRFIDReader();
}

void restartReserved() {
  user_uid = "";
  have_user_id = false;
  resetRFIDReader();
}

void setColor(int red, int green, bool blue) {
  analogWrite(RED, red);
  analogWrite(GREEN, green);
  if (blue) {
    digitalWrite(BLUE, HIGH);
  }
  else {
    digitalWrite(BLUE, LOW);
  }
}










