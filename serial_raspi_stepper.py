import serial
import os
#arduino_serial = serial.Serial('/dev/tty.usbserial',9600)#à changer sur Linux
class Stepper:
    def __init__(self,num):
        self.number = num
        self.filename = "stepper"+str(self.number)
        self.anglefile = open(self.filename,"w+")
        if os.stat(self.filename).st_size == 0:
            with open(self.filename,"w+") as file:
                file.write("0")
                file.close()
        if self.number < 10:
            self.numstr="0"+str(self.number)
        else:
            self.numstr=str(self.number)
    def write(self,angle):
        #arduino_serial.write(b("ST"+self.numstr+":"+str(angle)))
        print("writing to servo")
    def getangle(self):
        print(self.anglefile.readlines())
        #return float(self.anglefile.readlines()[0])
class Servo:
    def write(angle):
        pass
step01 = Stepper(1)
#step01.write(90)
step01.getangle()
#print(angle)
