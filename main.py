from machine import Pin, SPI
from sx127x import SX127x
import time
import struct

lora_parameters = {
    'frequency': 915E6,
    'bandwidth':125E3,
    'spreading_factor': 7,
    'coding_rate': 1,
    'preamble_length': 8,
    'tx_power': 14
}

lora_pins = {
    'dio_0':8,
    'ss':17,
    'reset':20,
    'sck':18,
    'miso':16,
    'mosi':19,
}

lora_spi = SPI(0, baudrate=5000000, polarity=0, phase=0, 
               bits=8, firstbit=SPI.MSB,
               sck=Pin(lora_pins['sck'], Pin.OUT, Pin.PULL_DOWN),
               mosi=Pin(lora_pins['mosi'], Pin.OUT, Pin.PULL_UP),
               miso=Pin(lora_pins['miso'], Pin.IN, Pin.PULL_UP))

lora = SX127x(lora_spi, pins=lora_pins, parameters=lora_parameters)

print("LoRa RX iniciado...")


# Loop principal
while True:
    if lora.receivedPacket():
        payload = lora.readPayload()

        print("Payload bruto:\t", payload)
        print("Tamanho do payload:\t", len(payload))
        
        # Verifica se é assim mesmo que pega os dados da struct
        temp_aht20, humi_aht20, temp_bmp280, press_bmp280 = struct.unpack('<ffff', payload)
        
        print("Temperatura AHT20:\t{:.2f} °C".format(temp_aht20))
        print("Umidade AHT20:\t{:.2f} %".format(humi_aht20))
        print("Temperatura BMP280:\t{:.2f} °C".format(temp_bmp280))
        print("Pressão BMP280:\t{:.2f} hPa".format(press_bmp280))
        print("-------------------------------")
    else:
        payload = lora.readPayload()
        print("Erro no recebimento!")
        print("Payload bruto:\t", payload)
        print("Tamanho do payload:\t", len(payload))
        print("-------------------------------")

    time.sleep(1)