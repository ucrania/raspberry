import time
import spidev


import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
#import Adafruit_GPIO as GPIO

import RPi.GPIO as GPIO

import Image
import ImageDraw
import ImageFont

import datetime
import sys
import os


GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN,  pull_up_down=GPIO.PUD_UP)

#inicializacao de variaveis
recebido=31.41
Auto='Automatico'


tanquexl=0
tanquexr=20
tanqueyb=5
tanqueyt=45
nivel=(tanqueyt-tanqueyt)-((recebido*4)/10)

# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0 #escolher o porto spi 0 ou 1 (GPIO 6/7)
ADC_DEVICE =1

# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi= SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

# Escolher contraste
disp.begin(contrast=60)

# Imagem Branca
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
draw = ImageDraw.Draw(image)
# Carregar fonts
font = ImageFont.load_default()

disp.image(image)
disp.display()

#draw.text((22,30),'%.2f %%' % (recebido), font=font)

spi =spidev.SpiDev()
spi.open(SPI_PORT,ADC_DEVICE)
spi.max_speed_hz = 10000000
spi.mode = 0b01
desligar=0
tdesligar=58

try:
        while True:
                if not GPIO.input(21) or desligar:
                        draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
                        if not desligar:
                                os.system('sudo shutdown')
                        draw.text((10,12),'A desligar', font=font)
                        draw.text((13,20),'em: %d Seg'%(tdesligar), font=font) 
                        disp.image(image)
                        disp.display()
                        desligar=1
                        time.sleep(1)
                        tdesligar=tdesligar-1
                        
                else:
                        draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
                        hatual=datetime.datetime.now().strftime('%H')
                        matual=datetime.datetime.now().strftime('%M')
                        satual=datetime.datetime.now().strftime('%S')
                        
                        
                        spi.xfer([0b10000000])
                        rec=spi.readbytes(2)
                        #print "ADC Result: ",rec
                        
                        total=rec[0]*255+rec[1]
                        tensao=float(total)*5/65535
                        #print 'Voltage= {0:.2f}'.format(tensao),
                        trega=(tensao*120+3) #calculo tempo de rega
                        hrega=(datetime.time((int)(trega/60),(int)(trega%60),0,0)).strftime('%H')
                        mrega=(datetime.time((int)(trega/60),(int)(trega%60),0,0)).strftime('%M')

                        phrega=20
                        pmrega=40
                        
                        nivel=40-((tensao*20*4)/10)
                        draw.rectangle((tanquexl,tanqueyb,tanquexr,tanqueyt),outline=0,fill=255)
                        draw.rectangle((tanquexl,(nivel+6),tanquexr,tanqueyt+1), outline=0, fill=0)
                        
                        draw.text((22,38),'%.2f %%' % (tensao*20), font=font)           #Nivel Agua

                        if (int)(hatual)>=(int)(phrega) & (int)(hatual)<=(int)(phrega)+(int)(hrega):
                                if (int)(hatual)==(int)(phrega):
                                        if (int)(matual)>=(int)(pmrega)+(int)(mrega):
                                                draw.text((67,38),'ON', font=font)
                                        else:
                                                draw.text((67,38),'OFF', font=font) 
                                else:
                                        draw.text((67,38),'ON', font=font)
                        else:
                                draw.text((67,38),'OFF', font=font)                             #estado da rega ON OFF

                        if GPIO.input(12):
                                if Auto=='Manual':
                                        Auto='Automatico'
                                else: 
                                        Auto='Manual'
                                time.sleep(0.33)
                                        
                        draw.text((22,30),Auto, font=font)                            #'06:30:00'
                        trega=(tensao*120+3) #calculo tempo de rega
                        
                        draw.text((22,22),'%s:%s:00'%(phrega,pmrega), font=font)                        #
                        draw.text((22,14),'', font=font)                                #Proxima 
                        
                        #print datetime.time((int)(trega/60),(int)(trega%60),0,0)
                        if trega>60:
                                draw.text((22, 6),'%dh %dmin' %((trega/60),(trega%60)), font=font)#Tempo de rega Horas
                        if trega<=60:
                                draw.text((22, 6),'%d Minutos' %trega, font=font)#Tempo de rega Minutos
                        
                        draw.text((22,-2),'%s:%s:%s'%(hatual,matual,satual), font=font)          #Hora atual
                                        
                        disp.image(image)
                        disp.display()
                        time.sleep(0.02)
		
		
except KeyboardInterrupt:
        spi.close() 
	sys.exit(0)

