from machine import Pin, SPI
import time

# Configuracion de pines
PIN_SCK = 18
PIN_MOSI = 23
PIN_MISO = 19
PIN_CS = 5
PIN_RST = 22

# Inicializar el reset en alto
rst = Pin(PIN_RST, Pin.OUT)
rst.value(1)


# Inicializar el chip select en alto
cs = Pin(PIN_CS, Pin.OUT)
cs.value(1)

# Inicializar el bus SPI
spi = SPI(1, baudrate=1000000, polarity=0, phase=0,
          sck=Pin(PIN_SCK), mosi=Pin(PIN_MOSI), miso=Pin(PIN_MISO))

def leer_registro(registro):
    cs.value(0)  # bajar CS: "ahora si te estoy hablando"
    # Para LEER un registro, el primer byte enviado debe tener el bit mas alto en 1,
    # y el registro va corrido 1 bit a la izquierda (asi funciona el protocolo del MFRC522)
    spi.write(bytes([((registro << 1) & 0x7E) | 0x80]))
    resultado = spi.read(1)  # leer 1 byte de respuesta
    cs.value(1)  # subir CS: "ya termine"
    return resultado[0]

time.sleep(0.1)  # pequena pausa para que el chip arranque bien

VERSION_REG = 0x37
version = leer_registro(VERSION_REG)
print("Version del MFRC522:", hex(version))