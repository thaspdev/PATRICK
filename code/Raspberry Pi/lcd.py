import RPi.GPIO as GPIO
import time


class Lcd:

    def __init__(self, PIN_RS, PIN_E, PIN_D4, PIN_D5, PIN_D6, PIN_D7):
        self.RS = PIN_RS
        self.E = PIN_E
        self.D4 = PIN_D4
        self.D5 = PIN_D5
        self.D6 = PIN_D6
        self.D7 = PIN_D7

        self.LARGEUR = 16
        self.CHR = True
        self.CMD = False

        self.LINE_1 = 0x80 #Code hexadécimal de la commande servant à forcer le curseur à aller à au début de la première
        self.LINE_2 = 0xC0 #Même chose pour la deuxième

        self.E_PULSE = 0.0005 #Délai entre le 1 et le 0
        self.E_DELAY = 0.0005 #Délai avant d'envoyer le premier signal puis après avoir envoyé le deuxième
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        #On précise ici le fait que l'on va utiliser tous ces pins en mode "sortie", c'est-à-dire qu'on ne fera que leur envoyer des impulsions (on ne lira pas leur valeur)
        GPIO.setup(self.RS, GPIO.OUT)
        GPIO.setup(self.E, GPIO.OUT)
        GPIO.setup(self.D4, GPIO.OUT)
        GPIO.setup(self.D5, GPIO.OUT)
        GPIO.setup(self.D6, GPIO.OUT)
        GPIO.setup(self.D7, GPIO.OUT)

        self.écrire(0x33,self.CMD) # 110011 Initialise
        self.écrire(0x32,self.CMD) # 110010 Initialise
        self.écrire(0x06,self.CMD) # 000110 Cursor move direction
        self.écrire(0x0C,self.CMD) # 001100 Display On,Cursor Off, Blink Off
        self.écrire(0x28,self.CMD) # On précise le mode d'utilisation de l'écran. Ici on lui fait savoir qu'on l'utilisera en 4 bits (avec 4 fils de transmission de données connectés) sur deux lignes
        self.écrire(0x01,self.CMD) # Cette commande permet d'effacer le contenu de l'écran
        time.sleep(self.E)

    def écrire(self, bits, mode):
        GPIO.output(self.RS, mode) #On envoie au pin RS le mode (c'est-à-dire soit commande, soit écriture)

        GPIO.output(self.D4, False) #On envoie aux pins de données la valeur 0 afin que cela soit leur valeur par défaut lors de l'écriture
        GPIO.output(self.D5, False)
        GPIO.output(self.D6, False)
        GPIO.output(self.D7, False)

        #Lors de l'utilisation de l'écran en mode 4 bits, on envoie d'abord les 4 bits de poids le pluis fort, puis on envoie les 4 autres
        #L'opérateur & renvoie son second terme si tous les bits valant 1 dans ce dernier valent aussi 1 dans le premier terme
        
        if bits&0b10000==0b10000:#On cherche donc ici à savoir si le 5e bit du nombre vaut 1
            GPIO.output(self.D4, True) #Si cela est le cas, on envoie 1 à l'écran
        if bits&0b100000==0b100000: #Même chose pour le 6e
            GPIO.output(self.D5, True)
        if bits&0b1000000==0b1000000: #Même chose pour le 7e
            GPIO.output(self.D6, True)
        if bits&0b1000000==0b1000000: #Même chose pour le 8e
            GPIO.output(self.D7, True)

        #On envoie 1 puis 0 à self.E, c'est à dire au pin E. Cela signifie que l'état du courant passe de passant à bloqué, (ou d'élevé à faible) ce que l'écran LCD comprend comme signifiant l'écriture de toutes les valeurs arrivant aux pins au moment au cet état est changé (on écrit dans le registre de l'écran)
        time.sleep(self.E_DELAY)
        GPIO.output(self.E, True)
        time.sleep(self.E_PULSE)
        GPIO.output(self.E, False)
        time.sleep(self.E_DELAY)

        GPIO.output(self.D4, False)
        GPIO.output(self.D5, False)
        GPIO.output(self.D6, False)
        GPIO.output(self.D7, False)
        
        if bits&0b01==0b01: #Même chose que précédemment pour le 1er bit
            GPIO.output(self.D4, True)
        if bits&0b10==0b10: #Même chose pour le 2e
            GPIO.output(self.D5, True)
        if bits&0b100==0b100: #Même chose pour le 3e
            GPIO.output(self.D6, True)
        if bits&0b1000==0b1000: #Même chose pour le 4e
            GPIO.output(self.D7, True)

        time.sleep(self.E_DELAY)
        GPIO.output(self.E, True)
        time.sleep(self.E_PULSE)
        GPIO.output(self.E, False)
        time.sleep(self.E_DELAY)
        
        
    def message(self, message, line):
        message = message.ljust(self.LARGEUR)#On ajuste le message à écrire à la largeur de l'écran, c'est-à-dire 16 caractères. Si ce dernier est trop grand, il sera coupé

        self.écrire(line, self.CMD)#On dit à l'écran sur quelle ligne écrire en précisant le code hexadécimal de la ligne en premier paramètre, puis le mode commande

        for lettre in message: #Étant donné que le message a été ajusté à la largeur de l'écran, on peut itérer directement sur chacune de ses lettres sans dépasser la largeur de l'écran (16)
            self.écrire(ord(lettre),self.CHR) #Le début de la table de caractères de l'afficheur LCD correspond à la table ASCII, on peut donc lui envoyer le codage ASCII (ou Unicode, qui est également le même pour le début, et c'est que renvoie la fonction ord) du caractère, suivi du mode caractère

    def bye(self):
        self.écrire(0x01, self.CMD) #Cette commande permet d'effacer le contenu de l'écran (comme déjà dit précédemment)
        GPIO.cleanup()
