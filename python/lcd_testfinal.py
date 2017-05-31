import time #Tempo Hora, data, etc
import spidev #SPI

import Adafruit_Nokia_LCD as LCD #LCD nokia
import Adafruit_GPIO.SPI as SPI #SPI
#import Adafruit_GPIO as GPIO

import RPi.GPIO as GPIO #Interacao GPIO Rasp

import Image 
import ImageDraw
import ImageFont

import datetime
import sys
import os

import socket
import signal

import smtplib

import threading #biblioteca de tread

#comunicao websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.websocket
import tornado.web

host='192.168.137.36' 

class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#criacao de socket para comunicacao arduino-raspberry pi
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
	return b''.join(chunks)
	
	


#-----------------Codigo web_socket---------------

class LedHandler(tornado.websocket.WebSocketHandler):
        def check_origin(self, origin):
		return True


	def open(self):
		print "connection opened from: {}".format(self.request.remote_ip)
		#self.write_message("connection opened")


	def on_close(self):
		print "connection closed"

	def on_message(self, message):
		print color.OKBLUE + "Message received websocket: {}".format(color.OKGREEN + message)
		#aqui metes as condicoes conforme a mensagem
		#self.write_message("Servidor Recebeu")
		msg_recebida=[""]
		msg_recebida=message.split(",")
		
		if msg_recebida !="":
			#Tempo rega	, Prox. rega , Man/Auto
			for i in msg_recebida[:]:
				check=False
				
				try:
					
					titulo=(i.split(':'))[0]
					dados= (i.split(':'))[1]
					#print color.OKBLUE +"\n\tTitulo:"+color.OKGREEN+"" + titulo
					#print color.OKBLUE +"\n\tDados:" +color.OKGREEN+"" + dados
					if titulo.startswith('TR'):
						check=True
						trega_web=dados #tempo rega
					elif titulo.startswith('PR'): #prox rega
						check=True
						#Extrai a hora e minutos de prox rega
						phrega=(dados.split('.'))[0] #horas
						pmrega= (dados.split('.'))[1] #minutos
					elif titulo.startswith('MO') and (dados=="Auto" or dados=="Manual"):
						check=True
						if dados =="A":
							auto_manual='Automatico'
						elif dados =="M":
							auto_manual='Manual'
					elif titulo.startswith('AL') and (dados=="ON" or dados=="OFF"):
						check=True
						if dados =="ON":
							mail_enable=True
						elif dados =="OFF":
							mail_enable=False
							
					elif titulo.startswith('GET') and dados=="DATA":
						#devolver=["050","OFF","10.24","50.10"]
						self.write_message("V:"+devolver[1]+",D:"+devolver[0]+",H:"+devolver[2]+",T:"+devolver[3])
						print "Dados enviados para a webpage."
					elif titulo.startswith('GET') and dados=="INIT":	
						print "Dados enviados para a webpage."

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
	
	
	
	
	
	
	
#-------Definicao Time Out rececao de dados---------	

def signal_handler(signum, frame):
	    print color.WARNING+"Time out!"
		#raise Exception("Timed out!")
	
	
#Rececao dados socket Arduino Raspberry pi------------	
	
def receber_socket():
#Creates a timeout and receive data
	signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(10)   # five seconds
	received_data=[""]
	try:
		received_data=socket_test.myreceive().split(",")

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
auto_manual='Automatico'


tanquexl=0
tanquexr=20
tanqueyb=5
tanqueyt=45
nivel=(tanqueyt-tanqueyt)-((recebido*4)/10)
mail_enable=False  #habilita envio de emails
mailwassent=False


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

#socket_test = MySocket()
#socket_test. __init__()
#socket_test.connect(host, port)


#if __name__ == "__main__":
#	tornado.options.parse_command_line()
#	app = tornado.web.Application(handlers=[(r"/", LedHandler)])
#	server = tornado.httpserver.HTTPServer(app)
#	server.listen(8000)
#	tornado.ioloop.IOLoop.instance().start()
#	server_webpage=open("ws//192.168.249.140:8000")
#	time.sleep(10) 

try:
		#Corre numa thread a parte
		def thread_webSocket():

			if __name__ == "__main__":
				tornado.options.parse_command_line()
				app = tornado.web.Application(handlers=[(r"/", LedHandler)])
				server = tornado.httpserver.HTTPServer(app)
				server.listen(8000)
				tornado.ioloop.IOLoop.instance().start()
				
		def thread_socket():
			socket_test = MySocket()
			socket_test. __init__()
			socket_test.connect(host, port)
				
		thread_web=threading.Thread(target=thread_webSocket)
		thread_web.daemon=True
		thread_web.start()
		
		thread=threading.Thread(target=thread_socket)
		thread.daemon=True
		thread.start()


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
			draw.text((22,38),"%d%%"%int(dep), font=font)           #Nivel Agua
                        
                        draw.text((67,38),"%s" %sensores[1], font=font) 
						
                        if GPIO.input(12):
                                if auto_manual=='Manual':
                                        auto_manual='Automatico'
                                else: 
                                        auto_manual='Manual'
                                time.sleep(0.33)
                                        
                        draw.text((22,30),auto_manual, font=font)                            #'06:30:00'
                        trega=(tensao*120+3) #calculo tempo de rega
                        
                        draw.text((22,22),'%s:%s:00'%(phrega,pmrega), font=font)                        #
                        draw.text((22,14),'', font=font)                                #Proxima 
                        
                        #print datetime.time((int)(trega/60),(int)(trega%60),0,0)
						#Imprime tempo de rega para o lcd
			trega_lcd=0
			if auto_manual=='Automatico':
				trega_lcd=trega_web
			elif auto_manual=='Manual': 	
				trega_lcd=trega
							
                        if trega_lcd>60:
                                draw.text((22, 6),'%dh %dmin' %((trega_lcd/60),(trega_lcd%60)), font=font)#Tempo de rega Horas
                        if trega_lcd<=60:
                                draw.text((22, 6),'%d Minutos' %trega_lcd, font=font)#Tempo de rega Minutos
						#---------------------------------
                        
                        draw.text((22,-2),'%s:%s:%s'%(hatual,matual,satual), font=font)          #Hora atual
                                        
                        disp.image(image)
                        disp.display()
                        time.sleep(0.001)
			#Envia dados atraves do socket para o arduino			
			if auto_manual=='Automatico':
				socket_test.mysend("T:%d:%d,P:%d:%d\n" %((trega_web/60),(trega_web%60),phrega,pmrega))
			elif auto_manual=='Manual': 			
				socket_test.mysend("T:%d:%d,P:%d:%d\n" %((trega/60),(trega%60),phrega,pmrega))
			time.sleep(0.001)
			
			#Envia dados servidor (Raspberry Pi) - Webpage --------------
			
			##Deposito	ON/OFF	Humidade	Temperatura
			#devolver=["050","OFF","10.24","50.10"]
			server_webpage.write_message("V:"+devolver[2]+",D:%d,H:%.2f,T:%.2f"%(devolver[1],devolver[2],devolver[3]))

			#Envia Email caso deposito inferior a 5 porcento
			if mail_enable:
				
				if int(dep)<5 and not mailwassent:
					server = smtplib.SMTP('smtp.gmail.com', 587)
					server.starttls()
					mymail="seic2017g2@gmail.com"
					mypass="seic2017321"
					igormail="ucrania95@gmail.com"
					tomail=igormail
					server.login(mymail, mypass)
					print color.WARNING+"Foi enviado email de Alerta."

					msg = "Alerta! O deposito encontra-se vazio.\nSent by RaspberryPI\nMade by: Igor Koval and Alexandre Correia"

					server.sendmail(mymail,tomail, msg)
					server.quit()
					mailwassent=True

				elif mailwassent and int(dep)>10:
					mailwassent=False
except KeyboardInterrupt:
        spi.close() 
	sys.exit(0)
	
	
	



		






