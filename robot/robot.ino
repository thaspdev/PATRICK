#include <math.h>
#include <Servo.h>
const int pinServo = 7;
const int moteur1[] = {4, 3};
const double vitesse_du_son = 343; //à 20 °C, c-à-d une température ambiante
Servo servo;
void setup() {
  // put your setup code here, to run once:
  servo.attach(pinServo);
  int i;
  for(i = 0; i < 2; i++){
    pinMode(moteur1[i], OUTPUT);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  double a = 0;
  double b = 0;
  double c = 2;
  double t1 = 0.220;
  double t2 = 0.350;
  double t3 = 0.360;
  calcul_ab(t1,t2,&a,&b);
  int beta = calcul_beta(a,b,c);
  servo.write(0);
  delay(3000);
  if (beta>=0) {
    servo.write(beta);
    digitalWrite(moteur1[0], HIGH);
    digitalWrite(moteur1[1], LOW);
    delay(3000);
  } else if (beta<0) {
    servo.write(180+beta);
    digitalWrite(moteur1[0], LOW);
    digitalWrite(moteur1[1], HIGH);
    delay(3000);
  }
}

int calcul_beta(double a, double b, double c){
  return cos((a*a+c*c-b*b)/2*a*c)*180/PI;
}

void calcul_ab(double temps_1er, double temps_2e, double *a, double *b){
  *b = temps_1er*vitesse_du_son/2;
  *a = temps_2e*vitesse_du_son/2;
}

bool cote_objet(double temps_2e, double temps_3e, bool cote_mesure) {//Si le côté de la mesure est vers la gauche, cote_mesure vaut 0, sinon 1
  //Si l'objet est vers la gauche, cote_objet vaut 0, sinon 1
  if(cote_mesure) {//S'il va vers la droite pour mesurer
    if(temps_2e < temps 3e) {
      //Alors l'objet est vers la gauche
      return 0;
    } else {
      //Alors l'objet est vers la droite
      return 1;
    }
  } else {
    if(temps_2e < temps 3e) {
      //Alors l'objet est vers la droite
      return 1;
    } else {
      //Alors l'objet est vers la gauche  
      return 0;
    }
  }
}
int angle_servo(bool cote_objet, int beta){
    if (cote_objet) {
      return beta;
    } else {
      return 180-beta;
    }
}

void tourner_et_avancer(bool cote_objet, int angle_servo) {
  servo.write(angle_servo);
  if (cote_objet) {
    tourner_moteur();  
  }
}
void tourner_moteur(bool sens){
  if(sens) {
    
  } else {
    
  }
}
