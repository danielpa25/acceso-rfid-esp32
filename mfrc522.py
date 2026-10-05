from machine import Pin, SPI
import time

# ===== Configuracion de pines =====
PIN_SCK = 18
PIN_MOSI = 23
PIN_MISO = 19
PIN_CS = 5
PIN_RST = 22

rst = Pin(PIN_RST, Pin.OUT)
rst.value(1)

cs = Pin(PIN_CS, Pin.OUT)
cs.value(1)

spi = SPI(1, baudrate=1000000, polarity=0, phase=0,
          sck=Pin(PIN_SCK), mosi=Pin(PIN_MOSI), miso=Pin(PIN_MISO))


# ===== Funciones base (las que ya conoces) =====
def leer_registro(registro):
    cs.value(0)
    spi.write(bytes([((registro << 1) & 0x7E) | 0x80]))
    resultado = spi.read(1)
    cs.value(1)
    return resultado[0]


def escribir_registro(registro, valor):
    cs.value(0)
    spi.write(bytes([(registro << 1) & 0x7E]))
    spi.write(bytes([valor]))
    cs.value(1)


# ===== Inicializacion del chip (configuracion de timer, antena, etc) =====
def inicializar_mfrc522():
    escribir_registro(0x2A, 0x8D)  # TModeReg
    escribir_registro(0x2B, 0x3E)  # TPrescalerReg
    escribir_registro(0x2D, 30)    # TReloadRegL
    escribir_registro(0x2C, 0)     # TReloadRegH
    escribir_registro(0x15, 0x40)  # TxASKReg
    escribir_registro(0x11, 0x3D)  # ModeReg

    valor = leer_registro(0x14)    # TxControlReg: encender antena
    if (valor & 0x03) != 0x03:
        escribir_registro(0x14, valor | 0x03)


# ===== Comunicacion de bajo nivel: enviar y recibir datos del FIFO =====
def _transceive(datos):
    escribir_registro(0x02, 0x77)  # ComIEnReg
    escribir_registro(0x04, 0x7F)  # CommIrqReg: limpiar banderas
    escribir_registro(0x0A, 0x80)  # FIFOLevelReg: flush
    escribir_registro(0x01, 0x00)  # CommandReg: Idle

    for byte in datos:
        escribir_registro(0x09, byte)  # FIFODataReg

    escribir_registro(0x01, 0x0C)  # CommandReg: Transceive

    valor_actual = leer_registro(0x0D)
    escribir_registro(0x0D, valor_actual | 0x80)  # StartSend

    intentos = 2000
    while intentos > 0:
        irq = leer_registro(0x04)
        if irq & 0x30:
            break
        intentos -= 1

    escribir_registro(0x0D, valor_actual & (~0x80) & 0xFF)  # detener StartSend

    if intentos == 0:
        return None, 0

    error = leer_registro(0x06)
    if error & 0x1B:
        return None, 0

    n = leer_registro(0x0A)  # FIFOLevelReg: cuantos bytes llegaron
    recibido = []
    for _ in range(n):
        recibido.append(leer_registro(0x09))

    return recibido, n


# ===== Fase 1: detectar presencia de tarjeta (REQA) =====
def detectar_tarjeta():
    escribir_registro(0x0D, 0x07)  # BitFramingReg: REQA son 7 bits
    recibido, n = _transceive([0x26])  # 0x26 = REQA
    return recibido is not None


# ===== Fase 2: anti-colision, extraer el UID =====
def leer_uid():
    escribir_registro(0x0D, 0x00)  # BitFramingReg: byte completo esta vez
    comando_anticolision = [0x93, 0x20]
    recibido, n = _transceive(comando_anticolision)

    if recibido is None or n != 5:
        return None

    # El 5to byte es checksum (XOR de los primeros 4) -- lo verificamos
    checksum = 0
    for b in recibido[:4]:
        checksum ^= b

    if checksum != recibido[4]:
        return None

    return recibido[:4]  # el UID real son los primeros 4 bytes


def uid_a_texto(uid_bytes):
    return "".join("{:02X}".format(b) for b in uid_bytes)
