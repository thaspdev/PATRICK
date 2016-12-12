//#include <Stepper.h>
//Stepper stepper01;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  String message = Serial.readString();
  int sepIndex = message.indexOf(":");
  String command = message.substring(0,sepIndex);
  String param = message.substring(sepIndex,message.length());
  if(command.indexOf("ST")>-1){
    int stepNumb = message.substring(1,3).toInt();
    Serial.print(stepNumb);
  }
}
