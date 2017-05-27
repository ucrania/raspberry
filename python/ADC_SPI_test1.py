import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_GPIO as GPIO
import RPI.GPIO as GPIO1

GPIO1.setmode(GPIO.BCM)
GPIO1.setup(CONV_PIN, GPIO.OUT)

# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
ADC_DEVICE =1 #escolher o porto spi 0 ou 1 (GPIO 8/7)
CONV_PIN = 26

# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
#leitura

GPIO1.output(CONV_PIN, GPIO1.HIGH) #set HIGH
spi_adc=SPI.SpiDev(SPI_PORT, ADC_DEVICE, max_speed_hz=10000000)
time.sleep(0.5)
GPIO1.output(CONV_PIN, GPIO1.LOW)#set LOW
print spi_adc.read(1600)

