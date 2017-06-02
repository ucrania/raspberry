import socket
import sys
import time
import signal

host='192.168.137.114' #104 mario 99 alex
port=23
msg='IGOR'
received_data=''

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
        	print "Enviado:"+msg[totalsent:]
		if sent == 0:
  	     		raise RuntimeError("socket connection broken")
		totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
	tamanho=20
        while bytes_recd <  tamanho:	    
	    #print "R1"
            chunk = self.sock.recv(min(tamanho - bytes_recd, 2048))
	    #print "R2"
            if chunk == b'':
                raise RuntimeError("socket connection broken")
	    chunks.append(chunk)
	    bytes_recd = bytes_recd + len(chunk)
	return (b''.join(chunks).split("."))

socket_test = MySocket()
socket_test. __init__()
socket_test.connect(host, 23) # 20-Mario    105-Alex

#while True:
#Sends data
socket_test.mysend('P%d' %(69))
socket_test.mysend('B%d\n' %(31))
time.sleep(0.5)

#Creates a timeout and receive data
def signal_handler(signum, frame):
    raise Exception("Timed out!")

#signal.signal(signal.SIGALRM, signal_handler)
#signal.alarm(10)   # five seconds
try:
	received_data=socket_test.myreceive()
	print received_data

except Exception, msg:
	print color.WARNING +"Timed out!"

#print received_data
#Checks received data

try:
	
	titulo=received_data.split(':')[0]
	dados=received_data.split(':')[1]
	print color.OKBLUE +"Titulo:"+color.OKGREEN+"" + titulo
	print color.OKBLUE +"Dados:" +color.OKGREEN+"" + dados
		
except Exception:
	print color.WARNING + "Dados nao recebidos!"
	print Exception

try:

	if titulo.startswith('DEPOSITO'):
		print titulo
        elif titulo.startswith('VALVULA'):
		print titulo
        elif titulo.startswith('HUMIDADE'):
		print titulo
        elif titulo.startswith('TEMPERATURA'):
		print titulo
	else:
		print color.ENDC + "Dados nao reconhecidos"
	
	print color.HEADER+"Recebido: "+color.OKGREEN+""+ received_data



except Exception:
	print color.WARNING + "Erro ao filtrar dados!"
        print Exception
