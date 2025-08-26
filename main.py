from machine import Pin, SPI
from sx127x import SX127x
import time
import struct

spi = SPI(1, baudrate=5000000, polarity=0, phase=0, sck=Pin(4), mosi=Pin(3), miso=Pin(2))

cs = Pin(5, Pin.OUT)
reset = Pin(6, Pin.OUT)
irq = Pin(7, Pin.IN)

lora = SX127x(spi, cs, reset, irq, 
              frequency=915E6,   
              bandwidth=125E3,
              spreading_factor=7,
              coding_rate=5,
              preamble_length=8,
              tx_power=14)

print("LoRa RX iniciado...")


# Loop principal
while True:
    if lora.received_packet():
        payload = lora.read_payload()

        print("Payload bruto:\t", payload)
        print("Tamanho do payload:\t", len(payload))
        
        # Verifica se é assim mesmo que pega os dados da struct
        temp_aht20, humi_aht20, temp_bmp280, press_bmp280 = struct.unpack('<ffff', payload)
        
        print("Temperatura AHT20:\t{:.2f} °C".format(temp_aht20))
        print("Umidade AHT20:\t{:.2f} %".format(humi_aht20))
        print("Temperatura BMP280:\t{:.2f} °C".format(temp_bmp280))
        print("Pressão BMP280:\t{:.2f} hPa".format(press_bmp280))
        print("-------------------------------")

    time.sleep(1)