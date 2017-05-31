import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.websocket
import tornado.web
import time
import threading
import json
import codecs


class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
			#devolver=["050","OFF","10.24","50.10"]
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
						devolver=["050","OFF","10.24","50.10"]
						self.write_message("V:"+devolver[1]+",D:"+devolver[0]+",H:"+devolver[2]+",T:"+devolver[3])
						print "Dados enviados para a batata."
					elif titulo.startswith('GET') and dados=="INIT":	

						teste_send=[0]*500
						for i in range(0, 500):
							teste_send[i]=i
						self.write_message("GRAFICOT:"+json.dumps(teste_send))
						print "init confirm."
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



			
def thread_webSocket():
	try:
		print "teste5"
		if __name__ == "__main__":
			print "teste6"
			tornado.options.parse_command_line()
			app = tornado.web.Application(handlers=[(r"/", LedHandler)])
			server = tornado.httpserver.HTTPServer(app)
			server.listen(8000)
			print "teste1"
			tornado.ioloop.IOLoop.instance().start()
			#pagina=open("ws//192.168.249.140:8000")
			#print "teste2"
			#pagina.write_message("mensagem")
			#time.sleep(1)
			
			#devolver=["050","OFF","10.24","50.10"]
			#pagina.write_message("V:"+devolver[2]+",D:%d,H:%.2f,T:%.2f"%(devolver[1],devolver[2],devolver[3]))
			#print "Dados enviados para a webpage."
	except KeyboardInterrupt:
		print "Programa interrompido"
		
thread_web=threading.Thread(target=thread_webSocket)
print "teste2"
thread_web.daemon=True
print "teste3"
thread_web.start()		
print "teste4"


#with codecs.open('log.txt','a') as f:
#    value = ('arduino1 '+receivedData1+'  arduino2'+receivedData2)
#    s = str(value)
#    f.write(s)
#    f.write('\n')
#    f.close()

#file = open("test.txt", "r")
#name = file.readline()
#pin = int(file.readline())
#file.close()


while True:
		time.sleep(3)
		


