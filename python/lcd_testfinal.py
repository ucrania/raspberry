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

import socket
import signal

host='192.168.137.134' 

class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class MySocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < len(msg):
        	sent = self.sock.send(msg[totalsent:])
        	print color.HEADER+"\n\tEnviado: "+color.OKGREEN+""+msg[totalsent:]
		if sent == 0:
  	     		raise RuntimeError("socket connection broken")
		totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
	tamanho=40
        while bytes_recd <  tamanho:	    
	    #print "R1"
            chunk = self.sock.recv(min(tamanho - bytes_recd, 2048))
	    #print "R2"
            if chunk == b'':
                raise RuntimeError("socket connection broken")
	    chunks.append(chunk)
	    bytes_recd = bytes_recd + len(chunk)
	return b''.join(chunks).split(",")
	
def signal_handler(signum, frame):
	    print color.WARNING+"Time out!"
		#raise Exception("Timed out!")
	
def receber_socket():
#Creates a timeout and receive data
	signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(10)   # five seconds
	received_data=[""]
	try:
		received_data=socket_test.myreceive()

	except Exception, msg:
		print color.WARNING +"Time out!"
#Checks received data
	
	if received_data !="":
		#Deposito	ON/OFF	Humidade	Temperatura
		devolver=["050","OFF","10.24","50.10"]
		for i in received_data[:]:
			check=False
			
			try:
				
				titulo=(i.split(':'))[0]
				dados= (i.split(':'))[1]
				#print color.OKBLUE +"\n\tTitulo:"+color.OKGREEN+"" + titulo
				#print color.OKBLUE +"\n\tDados:" +color.OKGREEN+"" + dados
				if titulo.startswith('D') and len(dados)==3:
					check=True
					devolver[0]=dados
				elif titulo.startswith('V') and (dados=="ON" or dados=="OFF"):
					check=True
					devolver[1]=dados
				elif titulo.startswith('H') and len(dados)==5:
					check=True
					devolver[2]=dados
				elif titulo.startswith('T') and len(dados)==5:
					check=True
					devolver[3]=dados
				else:
					check=False
					print ""
					#print color.WARNING +''+ titulo +" nao reconhecido!"
				
				if check:
					print color.OKBLUE+"\tRecebido:"+color.OKGREEN+""+i
				#print color.HEADER+"\n\tRecebido: "+color.OKGREEN+""+ received_data

			except Exception:
				#print ""
				print color.WARNING + "Erro ao filtrar dados!"
	        	#print Exception
	else: 
		print color.WARNING+"Dados nao recebidos"
		#devolver=""

	return devolver


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

# inicializacao de variaveis socket
#host='192.168.137.250' #104 mario 99 alex
port=23
received_data=''

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

socket_test = MySocket()
socket_test. __init__()
socket_test.connect(host, port) 

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
						
						
			sensores=receber_socket()				
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

                        phrega=19
                        pmrega=32
                        dep=sensores[0]
			
			
			nivel=40-(int(dep)*40)/100
                        draw.rectangle((tanquexl,tanqueyb,tanquexr,tanqueyt),outline=0,fill=255)
                        draw.rectangle((tanquexl,(nivel+6),tanquexr,tanqueyt+1), outline=0, fill=0)
                        
                        #draw.text((22,38),'%.2f %%' % D, font=font)           #Nivel Agua
			draw.text((22,38),""+dep, font=font)           #Nivel Agua
                        
                        draw.text((67,38),"%s" %sensores[1], font=font) 
						
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
                        time.sleep(0.001)
						
			socket_test.mysend("T:%d:%d,P:%d:%d\n" %((trega/60),(trega%60),phrega,pmrega))
			time.sleep(0.001)
except KeyboardInterrupt:
        spi.close() 
	sys.exit(0)

