#!/usr/bin/python3
import détection_visage as dv
import gestionnaire_menu as gm
import communication_arduino as ard
import communication_bluetooth as bt
import threading as th
import queue as qu

#On met à chaque fois 2 queues dans une liste (un tableau), celle à l'indice 0 (et donc en première position de la liste) correspondant à la communication patrick.py vers un autre thread et inversement pour celle à l'indice 1 (en deuxième position)
queue_gm = [qu.Queue() for i in range(2)]
queue_dv = [qu.Queue() for i in range(2)]
queue_ard = [qu.Queue() for i in range(2)]
queue_bt = [qu.Queue() for i in range(2)]

#On crée un thread pour chacun de ces quatre "sous-programmes", afin qu'ils puissent être exécutés en parallèle. Target correspond à la fonction que le thread doit exécuter, en l'occurence une fonction appelée thread dans chacun des fichiers, et args correspond aux arguments qu'admet cette fonction ; ici, la liste formée de deux queues correspondant à chacun des thread est passée en argument de cette fonction afin que le thread en question puisse communiquer avec le thread principal
thread_dv = th.Thread(target=dv.thread, args=(queue_dv,))
thread_gm = th.Thread(target=gm.thread, args=(queue_gm,))
thread_ard = th.Thread(target=ard.thread, args=(queue_ard,))
thread_bt = th.Thread(target=bt.thread, args=(queue_bt,))

#On démarre chacun de ces quatre threads
thread_dv.start()
thread_gm.start()
thread_ard.start()
thread_bt.start()



while True: #On effectue une boucle infinie, qui cherchera toujours à transmettre des messages d'un thread à un autre
    #Les instructions try et except permettent respectivement de tester un code pour l'une et d'effectuer des actions si le code testé a renvoyé une erreur. En effet, la fonction get d'une queue utilisée avec le paramètre block valant False permet de ne pas trop ralentir l'exécution du programme mais provoque une erreur (qu'il faut donc gérer) s'il n'y a aucun message
    try:
        message_gm = queue_gm[1].get(block=False) #On essaie d'obtenir un message du gestionnaire de menu
        if message_gm=="DV:STOP": #Si celui nous dit d'arrêter la détection de visage
            queue_dv[0].put(message_gm) #On transmet le message au thread de détection de visage
        elif message_gm=="DV:START": #Sinon si il nous dit la reprendre
            queue_dv[0].put(message_gm) #On la démarre aussi
    except:
        message_gm = "" #Sinon on donne la valeur "" (chaîne de caractères vide) à la variable gardant ce message en mémoire
    try:
        message_dv = queue_dv[1].get(block=False)
        if message_dv[:6] == "VISAGE": #Si le thread de détection de visage a détecté un visage
            queue_ard[0].put(message_dv) #On transmet le message (contenant notamment l'angle auquel se trouve ce visage) à l'arduino
    except:
        message_dv = "" #Même chose que précédemment
    try:
        message_bt = queue_bt[1].get(block=False)
        if message_bt[:9]=="ANDROIDBT:": #On vérifie ici si les dix premiers caractères de la chaîne de caractères (du message) envoyée 
            if message_bt[10:]=="AV-START":
                queue_ard[0].put("ARDUINO:MO:START")
            elif message_bt[10:]=="AV-STOP" or message_bt[10:]=="AR-STOP":
                queue_ard[0].put("ARDUINO:MO:STOP")
            elif message_bt[10:]=="AR-START":
                queue_ard[0].put("ARDUINO:MO:INV")
            elif message_bt[10:]=="RAG-START": #RAG signifie Rotation dans le sens des AiGuilles d'une montre
                queue_ard[0].put("SEQUENCE:RLE-START")
            elif message_bt[10:]=="RAG-STOP":
                queue_ard[0].put("SEQUENCE:RLE-STOP")
            elif message_bt[10:]=="RCA-START": #RCA signifie Rotation dans le sens Contraire à celui des Aiguilles d'une montre
                queue_ard[0].put("SEQUENCE:RLE-START")
            elif message_bt[10:]=="RCA-STOP":
                queue_ard[0].put("SEQUENCE:RLE-STOP")
    except:
        message_bt = "" #Même chose que précédemment
        
