#include <Arduino.h>
#include <Servo.h>
#include <Adafruit_NeoPixel.h>

// Pin to the Left Servo
#define pinLeftServo 5

// Pin to the Right Servo
#define pinRightServo 6

// Pin to the Status LED
#define pinStatusLed 9
#define NUMPIXELS 64 //Número de píxeles
#define DELAYVAL 1 //timpo de espera en ms 
Adafruit_NeoPixel pixels(NUMPIXELS, pinStatusLed, NEO_GRB + NEO_KHZ800);

Servo leftServo; // the servo used to control a camera that can look around the robot
Servo rightServo;

struct DATA {
    float servo;
    float status;
} received;

void setup() {
    Serial.begin(9600);
    leftServo.attach(pinLeftServo);
    rightServo.attach(pinRightServo);
    pixels.begin(); // Inicializamos el objeto "pixeles"
}

void loop() {
    pixels.clear(); // Apagamos todos los LEDs
    if (Serial.available() >= sizeof(uint8_t)) {
        delayMicroseconds(10);
        uint8_t cmd = (uint8_t) Serial.read();
        // SERVO MOTOR COMMAND
        if (cmd == 0) {
            Serial.readBytes((char *) &received.servo, sizeof(float));
            int left_angle=5+(int)received.servo;
            int right_angle=180-(int)received.servo;
            Serial.print("Left Servo: ");
            Serial.print(left_angle);
            Serial.print("Right Servo: ");
            Serial.print(right_angle);
            leftServo.write(left_angle);
            rightServo.write(right_angle);
        }
        // STATUS COMMAND
        else if (cmd == 2) {
            Serial.readBytes((char *) &received.status, sizeof(float));
            if ((int) received.status == 1){
                Serial.print("Blue: Teleoperation (Manually driving)");
                for(int i=0; i<NUMPIXELS; i++) {
                    pixels.setPixelColor(i, pixels.Color(0, 0, 255));
                    pixels.show();
                    delay(DELAYVAL);
                }
            }
            else if ((int) received.status == 2){
                Serial.print("Red: Autonomous operation");
                for(int i=0; i<NUMPIXELS; i++) {
                    pixels.setPixelColor(i, pixels.Color(255, 0, 0));
                    pixels.show();
                    delay(DELAYVAL);
                }
            }
            else if ((int) received.status == 3){
                Serial.print("# Flashing Green: Successful arrival at a post or passage through a gate");
                for(int i=0; i<NUMPIXELS; i++) {
                    pixels.setPixelColor(i, pixels.Color(0, 255, 0));
                    pixels.show();
                    delay(DELAYVAL);
                }
            }
        }
    }
}

