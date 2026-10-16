from machine import Pin
from network import WLAN, STA_IF
import time

LED1 = 2
led1 = Pin(LED1, Pin.OUT)
led1.value(0)

def wifiConnect(SSID, PASSWORD):

    wlan = WLAN(STA_IF)  # modo estacion

    wlan.active(False)  # apagar primero, por si quedo en un estado raro
    time.sleep(0.5)
    wlan.active(True)  # encender limpio
    time.sleep(0.1)

    if wlan.active(True) and not wlan.isconnected():

        wlan.connect(SSID, PASSWORD)

        intentos = 10
        while not wlan.isconnected() and intentos > 0:
            print("Conectando...")
            time.sleep(0.5)
            intentos -= 1

        if wlan.isconnected():
            print("Conectado! IP:", wlan.ifconfig()[0])
            led1.value(1)
        else:
            print("No se pudo conectar al WiFi")
            led1.value(0)
