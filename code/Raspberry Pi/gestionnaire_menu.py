import menu
import lcd
import time
import RPi.GPIO as GPIO

def thread(queue):
    
    OK_PIN = 10
    BACK_PIN = 11
    
    global face_detection_enabled
    face_detection_enabled = True

    def back_callback(channel):
        global current_menu
        global rootmenu
        print("appel de la fonction back")
        if current_menu == "bluetooth":
            global bluetooth_menu
            bluetooth_menu.unset_gpio()
            rootmenu.set_gpio()
            rootmenu.show()
            current_menu = "root"
        elif current_menu == "wi_fi":
            global wi_fi_menu
            wi_fi_menu.unset_gpio()
            rootmenu.set_gpio()
            rootmenu.show()
            current_menu = "root"

    def ok_callback(channel):
        print("appel de la fonction ok")
        global current_menu
        if current_menu == "root":
            action = rootmenu.getActionsList()[rootmenu.getCurrentIndex()]
            if action == "fd_toggle":
                global face_detection_enabled
                if face_detection_enabled:
                    print("Stopping face detection")
                    queue.put("FD:STOP")
                    rootmenu.setText(0,"Marche")
                    face_detection_enabled = False
                else:
                    print("Enabling face detection")
                    queue.put("FD:START")
                    rootmenu.setText(0,"Veille")
                    face_detection_enabled = True
                rootmenu.show()
            elif action == "bluetooth":
                rootmenu.unset_gpio()
                global bluetooth_menu
                bluetooth_menu = menu.Menu(lcd_screen,8,9,["Activer BT","bt_toggle"], ["Param BT","bt_settings"])
                current_menu = "bluetooth"
            elif action == "wi_fi":
                rootmenu.unset_gpio()
                global wi_fi_menu
                wi_fi_menu = menu.Menu(lcd_screen,8,9,["Activer Wi-Fi","wi_fi_toggle"], ["Param Wi-Fi","wi_fi_settings"])
                current_menu = "wi_fi"
                
        elif current_menu == "bluetooth":
            action = bluetooth_menu.getActionsList()[bluetooth_menu.getCurrentIndex()]
            if action == "bt_toggle":
                print("Toggling BT")
            elif action == "bt_settings":
                print("BT settings")
        elif current_menu == "wi_fi":
            action = wi_fi_menu.getActionsList()[wi_fi_menu.getCurrentIndex()]
            if action == "wi_fi_toggle":
                print("toggling wi_fi")
            elif action == "wi_fi_settings":
                print("wi_fi settings")
    lcd_screen = lcd.Lcd(2,3,4,5,6,7)
    global rootmenu
    rootmenu = menu.Menu(lcd_screen,8,9,["Veille","fd_toggle"],["Bluetooth","bluetooth"],["Wi-Fi","wi_fi"],["Parametres","settings"],["Eteindre","power_off"])
    global current_menu
    current_menu = "root"

    GPIO.setup(OK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(OK_PIN, GPIO.RISING, callback= ok_callback, bouncetime=300)
    
    GPIO.setup(BACK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(OK_PIN, GPIO.RISING, callback= ok_callback, bouncetime=300)
    
    #Exemple de ce que l'on pourrait faire
##    while True:
##        
##        for i in range(4):
##            time.sleep(0.3)
##            rootmenu.down()
##        for i in range(4):
##            time.sleep(0.3)
##            rootmenu.up()
