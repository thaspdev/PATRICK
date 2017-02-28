import arduino #On importe le fichier arduino.py
import time
def thread(queue): #queue permettant de communiquer avec le programme "central" (patrick.py)
    
    UNO = arduino.Arduino(2) #Création d'un objet représentant l'arduino
    
    stepper_caméra = arduino.Stepper(UNO,1) #Création d'un objet représentant le moteur pas à pas
    servo_caméra = arduino.Servo(UNO,1)
    
    servo_direction = arduino.Servo(UNO,2) #Création d'un objet représentant le servomoteur faisant tourner les roues
    time.sleep(0.1) #On met le programme en pause pendant 0,1 secondes afin d'éviter que SV:02:0 et SV:03:0 ne se retrouvent sur la même ligne dans l'information reçue en série (serial). En effet, lors de l'initialisation de ces objets, le programme envoie ces chaînes de caractères à l'Arduino afin qu'il place les servomoteurs en position zéro (cf. arduino.py). Si l'intervalle entre l'envoi de ces deux chaînes de caractères est trop court, l'Arduino considèrera qu'il aura reçu qu'une seule chaîne de caractères, composée de la concaténation des deux chaînes en question, ce qui causerait des problèmes dans l'analyse de la commande.
    servo_soulèvement_roues = arduino.Servo(UNO,3)#Création d'un objet représentant le servomoteur levant les roues
    moteur_roues = arduino.Moteur(UNO,1) #Crétion d'un objet représentant le moteur faisant tourner les roues
    
    patrick_message = "" #Message provenant de patrick.py
    sens_aiguilles_montre=True #Variable booléenne définissant le sens de rotation du moteur pas à pas
    temps_précédent = time.time() #Initialisation d'une variable
    delay=0.1 #Délai en secondes entre l'envoi des commandes au moteur pas à pas faisant tourner la caméra
    stepper_caméra_activé = True #Variable booléenne indiquant si le moteur pas à pas doit tourner à chaque itération de la boucle while suivante
    angle_servo_direction = 0 #angle qui sera donné au servomoteur lors du contrôle via un téléphone android
    while True: #Cette boucle est infinie afin que le programme  du Raspberry Pi puisse en permanence communiquer avec l'arduino
        try:
            patrick_message = queue[0].get(block=False) #On essaie d'obtenir un message (une chaîne de caractères) depuis la queue stockant les messages venant de patrick.py destinés à arduino_communication.py. Cependant, s'il n'y a pas de messsage, cela provoque une erreur lorque le paramètre block de la fonction get vaut faux (False). De plus, lorsque ce dernier vaut vrai (True), cette fonction get bloque le déroulement du programme jusqu'à recevoir un message, or, cette partie du programme ne doit pas être interrompue, auquel cas elle n'enverrait plus de signal au moteur pas à pas afin qu'il tourne, ce qui empêcherait à face_detection.py de bien détecter les visages
        except:
                patrick_message = "" #Si une erreur se produit, on donne à patrick_message la valeur "", c'est-à-dire une chaîne de caractères vide.
        if patrick_message[:7] == "VISAGE": #Si les 7 permiers caractères de patrick_message valent "VISAGE", alors cela signifie que détection_visage.py a détecté un visage à l'angle précisé dans la suite du message
            angle_stepper = int(stepper_caméra.obtenir_angle()*(2/3)) #On stocke l'angle du moteur pas à pas dans une variable. Il faut cependant noter le fait que cet angle est exprimé en nombre de pas (270 pour un demi-tour ; 540 pour un tour complet), et qu'on doit le convertir en degrés en le multipliant par $\color{red}\dfrac{2}{3}$ (En effet, $\color{red} 270 \times \dfrac{2}{3} = 180$ et $\color{red} 540 \times \dfrac{2}{3} = 360$
            angle_visage = float(patrick_message[8:]) #Le message étant de la forme "Visage:90" (pour un angle de 90 degrés, par exemple), l'angle se trouve dans la sous chaîne de caractères commençant à la position 8
            angle = stepper_angle + angle_visage #L'angle donné par le message est celui de la caméra. Cependant, pour obtenir l'angle duquel les roues doivent tourner, il faut lui ajouter l'angle du moteur pas à pas (cet angle est stocké dans un fichier et est défini arbitrairement, en fonction d'une droite donnant la position de l'angle 0 et étant la médiatrice sur un plan horizontal du côté du robot où se trouve la poignée)
            servo_soulèvement_roues.write(0) #On demande au servo
            if angle < 0 : # Si l'angle est négatif, on fait tourner les roues à un angle valant 180 degrés moins l'angle en question, puis on fait tourner le moteur en sens inverse
                servo_direction.write(180-angle)
                angle_servo_direction = 180 - angle #On change la valeur de angle_servo_direction afin que le contrôle via un téléphone puisse le modifier à partir de sa réelle valeur
                moteur_roues.tourner(inverse=True)
            else: #Sinon, on fait tourner les roues à l'angle en question puis on fait tourner le moteur dans le sens "normal"
                servo_direction.write(angle)
                angle_servo_direction
                moteur_roues.tourner(inverse=False)
            servo_soulèvement_roues.write(30) #On abaisse le servomoteur permettant de lever les roues afin que ces dernières soient en contact avec le sol
            moteur_tourne = True
            while moteur_tourne:
                patrick_message = queue[0].get(block=True) #On attend un message du thread principal
                if patrick_message == "FINVSG":#Quand on reçoit le bon message
                    moteur_tourne = False #On sort de la boucle, afin d'arrêter le moteur
            moteur_roues.stop()#On arrête le moteur
        elif patrick_message[:9] == "SEQUENCE:": #Pour le contrôle via Android. J'ai appelé cela "SEQUENCE" car il s'agit d'une séquence d'instructions que doit envoyer le Raspberry Pi à l'Arduino
            if patrick_message[10:] == "RAG-START": #RAG signifie Rotation dans le sens des AiGuilles d'une montre (RAG), START signifiant son début
                servo_soulèvement_roues.write(0) #On monte les roues afin qu'elles ne touchent pas le sol
                while patrick_message != "SEQUENCE:RAG-STOP": #on attend un signal signifiant la fin de la rotation
                    try:
                        patrick_message = queue[0].get(block=False)
                    except:
                        patrick_message = ""
                        if angle_servo_direction < 180:
                            angle_servo_direction += 5 #L'angle est augmenté de 5 car le délai (time.sleep(0.1)) ralentit l'augementation de cet angle, ce qui signifie que si l'utilisateur souhaite augmenter fortement cet angle, cela prendrait beaucoup trop de temps
                            servo_direction.write(angle_servo_direction)
                            time.sleep(0.1) #On attend un dixième de seconde afin de ne pas envoyer trop de commandes à la suite
                    servo_soulèvement_roues.write(0) #On baisse les roues après la rotation du servomoteur de direction
            elif patrick_message[10:] == "RCA-START": #Même chose pour la Rotation dans le sens Contraire à celui des Aiguilles d'une montre (RCA)
                    while patrick_message != "SEQUENCE:RCA-STOP": #on attend 
                            try:
                                    patrick_message = queue[0].get(block=False)
                            except:
                                    patrick_message = ""
                            if angle_servo_direction > 0:
                                    angle_servo_direction -= 5
                                    servo_soulèvement_roues.write(15)
                                    servo_direction.write(angle_servo_direction)
                                    servo_soulèvement_roues.write(0)
                        
        if stepper_caméra_activé:#cette partie doit être à nouveau testée
                while time.time() - temps_précédent < delay:#pause jusqu'à avoir dépassé le délai minimal entre deux rotations
                        continue#cette instruction sert à continuer la boucle ; en effet, le langage Python ne permet pas de "créer" une boucle vide 
                if sens_aiguilles_montre: 
                        stepper_caméra.write(stepper_caméra.obtenir_angle()+30)
                else:
                        stepper_caméra.write(stepper_caméra.obtenir_angle()-30)
                angle_stepper = stepper_caméra.obtenir_angle()
                if angle_stepper >= 270 or angle_stepper <= -270:
                    sens_aiguilles_montre = not sens_aiguilles_montre#si l'"angle" (en nombre de pas) du moteur pas à pas (angle_stepper) est trop grand ou trop petit, on inverse le sens de rotation de ce dernier 
                temps_précédent = time.time()
