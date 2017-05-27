import time

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
import Adafruit_GPIO as GPIO

import Image
import ImageDraw
import ImageFont


#valor do
recebido=61.58

# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0 #escolher o porto spi 0 ou 1 (GPIO 6/7)
ADC_DEVICE =1

# Raspberry Pi software SPI config:
#SCLK = 4
#DIN = 17
#DC = 23
#RST = 24
#CS = 8

# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
#leitura

#set HIGH
spi_adc=SPI.SpiDev(SPI_PORT, ADC_DEVICE, max_speed_hz=10000000)
time.sleep(0.5)
#set LOW
print spi_adc.read(1600)

# Software SPI usage (defaults to bit-bang SPI interface):
#disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)

# Initialize library.
disp.begin(contrast=60)

# Clear display.
disp.clear()
disp.display()


# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
tanquexl=2
tanquexr=20
tanqueyb=2
tanqueyt=40
nivel=40-((recebido*4)/10)
# Draw a white filled box to clear the image.
draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

#tanque
draw.rectangle((tanquexl,tanqueyb,tanquexr,tanqueyt), outline=0, fill=255)
#agua
draw.rectangle((tanquexl,(nivel+2),tanquexr,tanqueyt), outline=0, fill=0)

# Draw some shapes.
#draw.ellipse((2,2,22,22), outline=0, fill=255)
#draw.rectangle((24,2,44,22), outline=0, fill=255)
#draw.polygon([(46,22), (56,2), (66,22)], outline=0, fill=255)
#draw.line((68,22,81,2), fill=0)
#draw.line((68,2,81,22), fill=0)

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.
# Some nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

# Write some text.
draw.text((22,30),'%.2f %%' % (recebido), font=font)
#for x in range(0, 3):
#	time.sleep(x)
#	str="Nivel: %d" % (x)
#	draw.text((8,30),str, font=font)

# Display image.
disp.image(image)
disp.display()
