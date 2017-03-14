import lcd
import RPi.GPIO as GPIO

class Menu:

    def __init__(self, écran_lcd, HAUT, BAS, *args):
        self.LCD = écran_lcd

        self.HAUT = HAUT
        self.BAS = BAS

        GPIO.setup(self.HAUT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.BAS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        self.définirMenu(args)
        self.afficher()
        self.définirCallback()

    def définirCallback(self):
        GPIO.add_event_detect(self.HAUT, GPIO.RISING)
        GPIO.add_event_callback(self.HAUT, self.HAUT_callback)
        GPIO.add_event_detect(self.BAS, GPIO.RISING)
        GPIO.add_event_callback(self.BAS, self.BAS_callback)
    
    def définirMenu(self, strings_and_functions):
        self.LISTE_LIGNES, self.LISTE_FONCTIONS = [],[]
        for arg in strings_and_functions:
            self.LISTE_LIGNES.append(arg[0])
            self.LISTE_FONCTIONS.append(arg[1])
        
        if len(self.LISTE_LIGNES) == 0: #Si l'on essaye de créer un menu vide
            raise IndexError("Pas assez de paramètres pour créer un menu (menu vide)") #On renvoie une erreur indiquant qu'il manque des paramètres à la fonction afin de créer un menu

    def afficher(self):
        self.LCD.message("->" + self.LISTE_LIGNES[0],self.LCD.LIGNE_1)
        self.POSITION_ACTUELLE_LIGNE = 0
        if len(self.LISTE_LIGNES) > 1:
            self.LCD.message("  " + self.LISTE_LIGNES[1],self.LCD.LIGNE_2)

    def HAUT(self):
        if self.POSITION_ACTUELLE_LIGNE > 0:
            self.POSITION_ACTUELLE_LIGNE -= 1
            self.LCD.message("->" + self.LISTE_LIGNES[self.POSITION_ACTUELLE_LIGNE],self.LCD.LIGNE_1)
            self.LCD.message("  " + self.LISTE_LIGNES[self.POSITION_ACTUELLE_LIGNE+1],self.LCD.LIGNE_2)

    def BAS(self):
        if self.POSITION_ACTUELLE_LIGNE < len(self.LISTE_LIGNES)-1 and len(self.LISTE_LIGNES) > 1:
            self.POSITION_ACTUELLE_LIGNE += 1
            if self.POSITION_ACTUELLE_LIGNE +1 == len(self.LISTE_LIGNES):
                self.LCD.message("  " + self.LISTE_LIGNES[self.POSITION_ACTUELLE_LIGNE-1],self.LCD.LIGNE_1)
                self.LCD.message("->" + self.LISTE_LIGNES[self.POSITION_ACTUELLE_LIGNE],self.LCD.LIGNE_2)
            else:
                self.LCD.message("->" + self.LISTE_LIGNES[self.POSITION_ACTUELLE_LIGNE],self.LCD.LIGNE_1)
                self.LCD.message("  " + self.LISTE_LIGNES[self.POSITION_ACTUELLE_LIGNE+1],self.LCD.LIGNE_2)

    def HAUT_callback(self,channel): # GPIO.add_event_callback donne automatiquement à la fonction de callback un paramètre channel (indiquant le numéro du GPIO duquel provient le signal), il a donc fallu passer par l'intermédiaire de ces fonctions afin de ne pas avoir à modifier les "anciennes" (et donc de ne pas avoir à leur ajouter un paramètre channel)
        self.HAUT()

    def BAS_callback(self,channel):
        self.BAS()

    def définirTexte(self,position,texte):
        self.LISTE_LIGNES[position] = texte

    def obtenirCurrentIndex(self):
        return self.POSITION_ACTUELLE_LIGNE

    def obtenirListeActions(self):
        return self.LISTE_FONCTIONS

    def défaire_gpio(self):
        GPIO.remove_event_detect(self.BAS)
        GPIO.remove_event_detect(self.HAUT)

    def définir_gpio(self):
        GPIO.add_event_detect(self.HAUT, GPIO.RISING)
        GPIO.add_event_callback(self.HAUT, self.HAUT_callback)
        GPIO.add_event_detect(self.BAS, GPIO.RISING)
        GPIO.add_event_callback(self.BAS, self.BAS_callback)