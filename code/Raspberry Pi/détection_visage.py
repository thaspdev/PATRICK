from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 #Module OpenCV
import os

def thread(queue):

    activée = True #Variable permettant de savoir si la détection de visages est activée
    visage_détecté = False

    caméra = PiCamera()
    caméra.resolution = ( 640, 480 ) #On définit la résolution de l'image
    caméra.framerate = 60
    caméra.hflip=True #On retourne l'image envoyée par la caméra horizontalement,
    caméra.vflip=True #puis verticalement. En effet, sur le robot, la caméra est placée à l'envers
    captureCaméra = PiRGBArray( caméra, size=( 640, 480 ) )

    cascade_visage = cv2.CascadeClassifier('/home/pi/Programs/opencv/data/haarcascades/haarcascade_frontalface_alt.xml') #On charge le fichier permettant de détecter un visage

    visage_détecté = True
    
    while True:
        if activée:
            for frame in caméra.capture_continuous(captureCaméra, format="bgr", use_video_port=True ):

                image = frame.array

                gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #On crée une version de l'image en teintes de gris
                visages = cascade_visage.detectMultiScale(gris) #L'analyse d'une image en teintes de gris est plus rapide que celle d'une image en couleurs

                if not visage_détecté:
                    for ( x, y, l, h ) in visages: #Chaque visage détecté possède 4 coordonées, celles du rectangle l'encadrant (x;y) le point de départ, l la largeur, h la hauteur;
                            angle_visage = (32-((640-(x+l))/10))
                            queue[1].put("VISAGE:"+str(angle_visage))
                            visage_détecté = True
                            break
                elif len(visages) == 0:
                    queue[1].put("FINVSG")
                else:
                    visage_détecté = False
                        

                captureCaméra.truncate(0) #On vide le flux d'images

                try:                
                    message = queue[0].get(block=False)
                    print(message)
                    if message == "DV:STOP":
                        activée = False
                        break #On sort de la boucle for afin d'arrêter la capture d'images
                except:
                    continue
        else:
            message = queue[0].get(block=True)
            if message == "DV:START": #On attend un signal pour réactiver la détection de visages
                activée = True
