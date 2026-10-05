import mfrc522
import time

mfrc522.inicializar_mfrc522()
time.sleep(0.1)

while True:
    if mfrc522.detectar_tarjeta():
        uid = mfrc522.leer_uid()
        if uid:
            print("UID detectado:", mfrc522.uid_a_texto(uid))
    time.sleep(0.3)