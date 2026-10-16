import wifimodule
import nfc



SSID = "TIGO0D2994"
PASSWORD = "XASN5AHP"

wifimodule.wifiConnect(SSID, PASSWORD)

while True:
    nfc.nfcReading()