import spidev
#import RPi.GPIO as GPIO
import time

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
import Adafruit_GPIO as GPIO

import Image
import ImageDraw
import ImageFont

# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0 #escolher o porto spi 0 ou 1 (GPIO 6/7)
ADC_DEVICE =1

# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
#leitura

disp.begin(contrast=60)
disp.clear()
disp.display()
font = ImageFont.load_default()

# Create blank image for drawing.
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
tanquexl=2
tanquexr=20
tanqueyb=2
tanqueyt=40


#tanque
draw.rectangle((tanquexl,tanqueyb,tanquexr,tanqueyt), outline=0, fill=255)
#agua
#draw.rectangle((tanquexl,(nivel+2),tanquexr,tanqueyt), outline=0, fill=0)


#draw.text((22,30),'%.2f %%' % (recebido), font=font)
#disp.image(image)
#disp.display()

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(ss, GPIO.OUT,initial=1)


spi =spidev.SpiDev()
spi.open(SPI_PORT,ADC_DEVICE)
spi.max_speed_hz = 10000000
spi.mode = 0b01

#GPIO.output(ss, 0)

print 'Enviado'
print spi.xfer([0b10000000])
print 'Recebido: '
recebido=spi.readbytes(2)

try:
        while True:
	    	spi.xfer([0b10000000])
            	rec=spi.readbytes(2)
		print "ADC Result: ",rec
            	time.sleep(0.02)
		total=rec[0]*255+rec[1]
		tensao=float(total)*5/65535
		print 'Voltage= {0:.2f}'.format(tensao),
	    	
		nivel=40-((tensao*20*4)/10)
		draw.rectangle((tanquexl,(nivel+2),tanquexr,tanqueyt), outline=0, fill=0)
		draw.text((22,30),'%.2f %%' % (tensao*20), font=font)
		
		disp.clear()
		disp.image(image)
		disp.display()

except KeyboardInterrupt:
        spi.close() 
        sys.exit(0)

