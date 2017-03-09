import serial  # bibliothèque permettant la communication série
import time    # pour le délai d'attente entre les messages
import os      # Pour s'assurer du fait que le fichier du stepper soit bien vide

class Arduino:

    def __init__(self,DEVICE): #fonction d'initialisation -> self représente l'objet (il est passé en paramètre de "sa" fonction d'initialisation)
        self.DEV = DEVICE
        if self.DEV == 0:#Si le paramaètre vaut 0, on essaye de "se connecter" uniquement à l'arduino sur /dev/ttyAMC0
            try:
                self.serial = serial.Serial('/dev/ttyACM0', 9600)
            except:
                raise ConnectionError("Connexion à l'Arduino impossible. Essayez de vous connecter à ACM1 au lieu de ACM0, en utilisant le paramètre 1 de la fonction.")
        elif self.DEV == 1:#Si le paramaètre vaut 1, on essaye de "se connecter" uniquement à l'arduino sur /dev/ttyAMC1
            try:
                self.serial = serial.Serial('/dev/ttyACM1', 9600)
            except:
                raise ConnectionError("Connexion à l'Arduino impossible. Essayez de vous connecter à ACM1 au lieu de ACM0, en utilisant le paramètre 0 de la fonction.")
        else:#Sinon, on essaye de "se connecter" sur /dev/ttyAMC0 puis /dev/ttyAMC1 si le premier ne fonctionnne pas
            try:
                self.serial = serial.Serial('/dev/ttyACM0', 9600)
            except:
                try:
                    self.serial = serial.Serial('/dev/ttyACM1', 9600)
                except:
                    raise ConnectionError("Connexion à l'Arduino impossible. Vous pouvez vérifier cela en tapant la commande \"ls /dev/ | grep ACM\" dans votre terminal.")
        
    def message(self, message, delay = 1):#cette fonction sert à communiquer avec l'arduino (lui envoyer un message)
        time.sleep(delay)
        self.serial.setDTR(level=0)
        self.serial.write(bytes(str(message),'ASCII'))

class Stepper:#moteur pas à pas
    def __init__(self,arduino,num): #fonction d'initialisation
        self.arduino = arduino #on spécifie l'arudino (l'objet) sur lequel est connecté le moteur
        self.number = num #on spécifie le numéro du moteur
        self.nom_du_fichier = "stepper"+str(self.number) #nom du fichier qui va stocker l'angle
        self.anglefile = open(self.nom_du_fichier,'r')#peut être optimisé
        self.numstr=""#Numéro du moteur pas à pas en version chaîne de caractères, 1 devient 01, 2 devient 02 etc., mais 10 reste 10, 11 reste 11 etc.
        if self.number < 10:
            self.numstr="0"+str(self.number)
        else:
            self.numstr=str(self.number)
        self.write(0)
##        with open(self.nom_du_fichier,'w') as file:
##            if os.stat(self.nom_du_fichier) == 0:
##                file.seek(0,0)
##                file.truncate()
##                file.write("0")
##                file.close()
    
    def write(self,angle):#fonction servant à donner un angle au stepper
        angle_to_add = angle - self.getangle() #l'angle à ajouter vaut l'angle à donner moins l'angle actuel 
        with open(self.nom_du_fichier,'w') as file: #on modifie l'angle dans le fichier
            file.seek(0,0)#On place le curseur en position 0 de la première ligne du fichier
            file.truncate()#On efface tout le texte se trouvant après le curseur (c'est-à-dire, ici, tout le texte)
            file.write(str(angle))#On écrit l'angle choisi
            file.close()#On ferme le fichier
        writestr = "ST" + self.numstr + ":" + str(angle_to_add) #chaîne de caractères envoyée à l'arduino afin de faire tourner le stepper
        self.arduino.message(writestr) #on envoie la chaîne
    
    def getangle(self): #fonction servant à obtenir l'angle en question
        if len(self.anglefile.readlines()) > 0: #si il y a un angle écrit dans le fichier
##            print(self.anglefile.readlines()) #débogage
            with open(self.nom_du_fichier,"r") as file:
                return float(file.readlines()[0]) #on retourne l'angle
        else:
            return 0 #sinon on retourne 0


class Servo:#servo moteur

    def __init__(self, arduino, num): #fonction d'initialisation
        self.number = num #on spécifie le numéro du servo
        self.arduino = arduino #on spécifie l'arudino (l'objet) sur lequel est connecté le servo
        self.numstr=""
        if self.number < 10:
            self.numstr="0"+str(self.number)
        else:
            self.numstr=str(self.number)
        self.write(0) #on initialise le servo à 0

    def write(self, angle): #fonction servant à écrire un angle
        strtowrite = "SV" + ":" + self.numstr + ":" + str(angle) #chaîne de caractères envoyée à l'arduino afin de faire tourner le servo
        self.arduino.message(strtowrite) #on envoie la chaîne


class Motor:
    
    def __init__(self, arduino, num): #fonction d'initialisation
        self.number = num #on spécifie le numéro du moteur
        self.arduino = arduino #on spécifie l'arudino (l'objet) sur lequel est connecté le moteur
        self.numstr = ""
        if self.number < 10:
            self.numstr="0"+str(self.number)
        else:
            self.numstr=str(self.number)

    def turn(self,reverse=False): #fonction servant à faire tourner le moteur
        if reverse:#si reverse est vrai, on fait tourner le moteur dans le sens inverse
            comm = "REV"
        else:
            comm = "START" #normal
        strtowrite = "MO" + ":" + self.numstr + ":" + comm
        self.arduino.message(strtowrite)

    def stop(self): #fonction servant à arrêter le moteur
        strtowrite = "MO" + ":" + self.numstr + ":STOP"
        self.arduino.message(strtowrite)
