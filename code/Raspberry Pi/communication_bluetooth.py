#!/usr/bin/python3
import bluetooth

def thread(queue):

    boucle = True

    while boucle:

        detection = True

        while detection:
            socket_serveur=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            port = 0
            socket_serveur.bind(("",port))
            socket_serveur.listen(1)

            uuid = "00001101-0000-1000-8000-00805F9B34FB"
            bluetooth.advertise_service( socket_serveur, "Bluetooth PATRICK", uuid )

            socket_client,address = socket_serveur.accept()
            print("Connexion avec ",address)

            données = socket_client.recv(1024)
            str_reçue = données.decode("utf-8")
            if str_reçue == "TELEPHONEANDROIDVERSPATRICK": #On s'assure du fait que le robot est bien contacté par un téléphone Android (même si cette vérification peut être facilement contournée)
                detection = False
            else: #Sinon on recommence le processus de détection
                print("Contact par un appareil non autorisé.")
                socket_serveur.close()

        connexion_terminée = False
        
        while not connexion_terminée:
            données = socket_client.recv(1024)
            str_reçue = données.decode("utf-8")
            if str_reçue != "":
                queue[1].put(str_reçue)
            if str_reçue == "FIN_CONNEXION":
                connexion_terminée = True

        socket_client.close()
        socket_serveur.close()
        
        try:
            message_patrick = queue[0].get(block=False)
            if message_patrick == "BT:STOP":
                while message_patrick != "BT:DÉMARRER":
                   message_patrick = queue[0].get(block=True) 
        except:
            message_patrick = ""
