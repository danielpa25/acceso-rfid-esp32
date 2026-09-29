from machine import Pin
from time import sleep

led = Pin(12, Pin.OUT)
led1 = Pin(2, Pin.OUT)

while True:
    led.value(1)
    led1.value(0)
    sleep(0.25)
    led.value(0)
    led1.value(1)
    sleep(0.25)