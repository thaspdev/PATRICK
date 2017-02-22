#include <Servo.h> //On inclut la librairie Servo permettant de contrôler un servomoteur
String commande;
String param;
int numberIndex;
int motors[][2]= {{7,8}};
int steppers[][4] = {{2,3,4,5}};
Servo camServo;
Servo liftServo;
Servo dirServo;//6: caméra ; 9 direction ; 10 soulever les roues
int del = 5;//délai en millisecondes entre les commandes données au moteur pas à pas (stepper) afin que ce dernier tourne
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); //On démarre la communication en série afin de pouvoir recevoir des commandes du Raspberry Pi
  camServo.attach(6); //On affecte un pin spécifique à chacun des servomoteurs
  liftServo.attach(10);
  dirServo.attach(9);
  for (int i = 0; i < sizeof(motors)/sizeof(motors[0]); i++) {
    for (int j = 0; j < sizeof(motors[0])/sizeof(motors[0][0]); j++) {
      pinMode(motors[i][j], OUTPUT);
    }
  }
  for (int i = 0; i < sizeof(steppers)/sizeof(steppers[0]); i++) {
    for (int j = 0; j < sizeof(steppers[0])/sizeof(steppers[0][0]); j++) {
      pinMode(steppers[i][j], OUTPUT);
    }
  }
}
void loop() {
  // put your main code here, to run repeatedly:
  obtenirCommande(); //Cette fonction sert à recevoir une commande du Raspberry Pi
  exécuterActionSuivante(); //Celle-ci execute l'action
  photores(); //Cette fonction détermine s'il faut allumer les LEDs afin d'éclairer les visages à détecter
}
void obtenirCommande() {
  commande=Serial.readString();
}
void exécuterActionSuivante() {
    //Commande du type MO:01:START
    //Index:           0123456789{10}
    if (commande.substring(0,2) == "MO") {
      numberIndex=commande.substring(3,5).toInt()-1;
      param=commande.substring(6);
      int curMotor[] = {motors[numberIndex][0],motors[numberIndex][1]};
      if (param.substring(0,5) == "START") {
        digitalWrite(curMotor[0],HIGH);
        digitalWrite(curMotor[1],LOW);
      } else if (param.substring(0,3) == "REV") {
        digitalWrite(curMotor[0],LOW);
        digitalWrite(curMotor[1],HIGH);
      } else if (param.substring(0,4) == "STOP") {
        digitalWrite(curMotor[0],LOW);
        digitalWrite(curMotor[1],LOW);
      }
    } else if (commande.substring(0,2) == "SV") {
      numberIndex=commande.substring(3,5).toInt();
      int angle=commande.substring(6).toInt();
      if (numberIndex == 1){
        camServo.write(angle);
      } else if (numberIndex == 2){
        liftServo.write(angle);
      } else if (numberIndex == 3) {
        dirServo.write(angle);
      }
    } else if (commande.substring(0,2) == "ST") {
      Serial.println("ST");
      numberIndex=commande.substring(3,5).toInt()-1;
      int angle = commande.substring(6).toInt();
      
      if(numberIndex<sizeof(steppers)/sizeof(steppers[0])){
      if (angle > 0){
        for (int i = 0; i < angle;i++) {
          //Serial.println(i);
          digitalWrite(steppers[numberIndex][0], HIGH); 
          digitalWrite(steppers[numberIndex][1], LOW);
          digitalWrite(steppers[numberIndex][2], LOW);
          digitalWrite(steppers[numberIndex][3], LOW);
          delay(del);
          digitalWrite(steppers[numberIndex][0], HIGH); 
          digitalWrite(steppers[numberIndex][1], HIGH);
          digitalWrite(steppers[numberIndex][2], LOW);
          digitalWrite(steppers[numberIndex][3], LOW);
          delay(del);
          digitalWrite(steppers[numberIndex][0], LOW); 
          digitalWrite(steppers[numberIndex][1], HIGH);
          digitalWrite(steppers[numberIndex][2], LOW);
          digitalWrite(steppers[numberIndex][3], LOW);
          delay(del);
          digitalWrite(steppers[numberIndex][0], LOW); 
          digitalWrite(steppers[numberIndex][1], HIGH);
          digitalWrite(steppers[numberIndex][2], HIGH);
          digitalWrite(steppers[numberIndex][3], LOW);
          delay(del);
          digitalWrite(steppers[numberIndex][0], LOW); 
          digitalWrite(steppers[numberIndex][1], LOW);
          digitalWrite(steppers[numberIndex][2], HIGH);
          digitalWrite(steppers[numberIndex][3], LOW);
          delay(del);
          digitalWrite(steppers[numberIndex][0], LOW); 
          digitalWrite(steppers[numberIndex][1], LOW);
          digitalWrite(steppers[numberIndex][2], HIGH);
          digitalWrite(steppers[numberIndex][3], HIGH);
          delay(del);
          digitalWrite(steppers[numberIndex][0], LOW); 
          digitalWrite(steppers[numberIndex][1], LOW);
          digitalWrite(steppers[numberIndex][2], LOW);
          digitalWrite(steppers[numberIndex][3], HIGH);
          delay(del);
          digitalWrite(steppers[numberIndex][0], HIGH); 
          digitalWrite(steppers[numberIndex][1], LOW);
          digitalWrite(steppers[numberIndex][2], LOW);
          digitalWrite(steppers[numberIndex][3], HIGH);
        }
      } else {
        for (int i = 0; i > angle; i--) {
          //Serial.println(i);
          digitalWrite(steppers[numberIndex][0], LOW); 
          digitalWrite(steppers[numberIndex][1], LOW);
          digitalWrite(steppers[numberIndex][2], LOW);
          digitalWrite(steppers[numberIndex][3], HIGH);
          delay(del);
          digitalWrite(steppers[numberIndex][0], LOW); 
          digitalWrite(steppers[numberIndex][1], LOW);
          digitalWrite(steppers[numberIndex][2], HIGH);
          digitalWrite(steppers[numberIndex][3], HIGH);
          delay(del);
          digitalWrite(steppers[numberIndex][0], LOW); 
          digitalWrite(steppers[numberIndex][1], LOW);
          digitalWrite(steppers[numberIndex][2], HIGH);
          digitalWrite(steppers[numberIndex][3], LOW);
          delay(del);
          digitalWrite(steppers[numberIndex][0], LOW); 
          digitalWrite(steppers[numberIndex][1], HIGH);
          digitalWrite(steppers[numberIndex][2], HIGH);
          digitalWrite(steppers[numberIndex][3], LOW);
          delay(del);
          digitalWrite(steppers[numberIndex][0], LOW); 
          digitalWrite(steppers[numberIndex][1], HIGH);
          digitalWrite(steppers[numberIndex][2], LOW);
          digitalWrite(steppers[numberIndex][3], LOW);
          delay(del);
          digitalWrite(steppers[numberIndex][0], HIGH); 
          digitalWrite(steppers[numberIndex][1], HIGH);
          digitalWrite(steppers[numberIndex][2], LOW);
          digitalWrite(steppers[numberIndex][3], LOW);
          delay(del);
          digitalWrite(steppers[numberIndex][0], HIGH); 
          digitalWrite(steppers[numberIndex][1], LOW);
          digitalWrite(steppers[numberIndex][2], LOW);
          digitalWrite(steppers[numberIndex][3], LOW);
          delay(del);
          digitalWrite(steppers[numberIndex][0], HIGH); 
          digitalWrite(steppers[numberIndex][1], LOW);
          digitalWrite(steppers[numberIndex][2], LOW);
          digitalWrite(steppers[numberIndex][3], HIGH);
        }
      }
    }
  }
}
void photores() {
  int lum = analogRead(0);
  if (lum < 500) { //Nous avons déterminé que si cette valeur, pouvant aller jusqu'à 1023, était inférieure à 500, il fallait éclairer les visages à détecter
    for (int pinLED = 1; pinLED <= 4; l++) {    
          digitalWrite(pinLED, HIGH); //On allume les 4 LEDs
        }
  }
}