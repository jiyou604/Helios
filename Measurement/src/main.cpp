#include <Arduino.h>
#include <time.h>
#include <HX711.h>


const int TS_CH1 = 34;
const int PS_CH1 = 35;
const int IG_CH1 = 12;
const int LOADCELL_DOUT_PIN = 2;
const int LOADCELL_SCK_PIN = 0;

HX711 scale;

float temperature;
float pressure;
float thrust;
float ignition_time;
float zero = 1020;
bool IG_flag = false;

// put function declarations here:
float get_temp(void);
float get_press(void);
float get_thrust(void);
void zero_press(void);
void ignition(void);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  pinMode(IG_CH1, OUTPUT);
  analogReadResolution(12);
  digitalWrite(IG_CH1, LOW);
  Serial.println("Initialization Done!!");
  scale.tare();

  temperature = get_temp();
  pressure = get_press();
  thrust = get_thrust();

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" *C");

  Serial.print("Pressure: ");
  Serial.print(pressure);
  Serial.println(" bar");

  Serial.print("Thrust: ");
  Serial.print(thrust);
  Serial.println(" kg");
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    String mode = Serial.readString();
  }
  temperature = get_temp();
  pressure = get_press();
  thrust = get_thrust();

  float time = millis()*0.001;

  Serial.print(temperature);
  Serial.print(",");
  Serial.print(pressure);
  Serial.print(",");
  Serial.print(thrust);
  Serial.print(",");
  Serial.print(time);
  Serial.print("\n");

  if (time - ignition_time>=2.5){
    digitalWrite(IG_CH1, LOW);
  }

    delay(50);
}

// put function definitions here:
float get_temp(void) {
  float voltage = analogReadMilliVolts(TS_CH1);
  return (voltage*0.001 - 1.25) / 0.005;
}

float get_press(void) {
  int raw = analogRead(PS_CH1);
  return (raw-zero)/31.496+1.00;
}

float get_thrust(void) {
  long raw;
  if (scale.wait_ready_timeout(1000)) {
    raw = scale.read();
  } else {
    Serial.println("HX711 not found.");
  }
  return raw/73324.53-3.3542;
}

void zero_press(void) {
  int sum = 0;
  for(int i = 0; i < 10; i++){
    sum += analogRead(PS_CH1);
  }
  zero = sum/10.0;
}
