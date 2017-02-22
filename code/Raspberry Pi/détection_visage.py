from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 #Module OpenCV
import os

def thread(queue):

    activée = True #Variable permettant de savoir si la détection de visages est activée
    visage_détecté = False

    camera = PiCamera()
    camera.resolution = ( 640, 480 )
    camera.framerate = 60
    camera.hflip=True #On retourne l'image envoyée par la caméra horizontalement,
    camera.vflip=True #puis verticalement. En effet, sur le robot, la caméra est placée à l'envers
    rawCapture = PiRGBArray( camera, size=( 640, 480 ) )

    face_cascade = cv2.CascadeClassifier('/home/pi/Programs/opencv/data/haarcascades/haarcascade_frontalface_alt.xml') #On charge le fichier permettant de détecter un visage

    temps_démarrage = time.time()
    
    while True:
        if activée:
            for frame in rawCapture, format="bgr", use_video_port=True ):

                image = frame.array

                gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #On crée une version de l'image en teintes de gris

                if not face_detected:
                    visages = face_cascade.detectMultiScale(gris) #L'analyse d'une image en teintes de gris est plus rapide que celle d'une image en couleurs

                    for ( x, y, l, h ) in visages: #Chaque visage détecté possède 4 coordonées, celles du rectangle l'encadrant ; 
                        if not face_detected:
                            face_angle = (32-((640-(x+l))/10))
                            face_detected = True
                            profile_face_detected = False
                            time_face_detected = time.time()
                            queue[1].put("VISAGE:"+str(face_angle))
                            

                rawCapture.truncate(0) #On vide le flux d'images

                try:                
                    message = queue[0].get(block=False)
                    print(message)
                    if message == "DV:STOP":
                        enabled = False
                        break #On sort de la boucle for afin d'arrêter la capture d'images
                except:
                    continue
        else:
            message = queue[0].get(block=True)
            if message == "DV:START": #On attend un signal pour réactiver la détection de visages
                enabled = True
