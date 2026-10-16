from machine import Pin
import mfrc522
import time

Lista_UIDs = ["2AF56EE1",
             "0ABDDC35",
             "CF8C21B7",
             "DDABF51D",
             "01020304"]

LED2 = 12
led2 = Pin(LED2, Pin.OUT)

mfrc522.inicializar_mfrc522()
time.sleep(0.1)

def nfcReading():
    if mfrc522.detectar_tarjeta():

        mfrc522.rst.value(1)
        uid = mfrc522.leer_uid()
        if uid:
            print("UID detected:", mfrc522.uid_a_texto(uid))

            if mfrc522.uid_a_texto(uid) in Lista_UIDs:

                print("UID Permitted")

                led2.value(1)
                time.sleep(1)
                led2.value(0)

            else:
                print("UID invalid")

    time.sleep(0.3)