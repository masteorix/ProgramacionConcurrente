import threading
import sys
import socket
import pickle
import os

class Cliente():

	def __init__(self, host=input("Intoduzca la IP del servidor ?  "), port=int(input("Intoduzca el PUERTO del servidor ?  ")),nickname=input("Cual es tu nickname ? ")):
		self.s = socket.socket()
		self.s.connect((host, int(port)))
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
		threading.Thread(target=self.recibir, daemon=True).start()

		while True:
			msg =input('\nEscriba texto ?   ** Enviar = ENTER   ** Salir Chat = 1 \n')
			with open("u22045519.txt", "a") as f:
				f.write("\n" + nickname + ":" + msg)
				f.close()
			if msg != '1' : 
				msg =nickname+ ":  " + msg
				self.enviar(msg)
			else:
				print(" **** Me piro vampiro; cierro socket y mato al CLIENTE con PID = ", os.getpid())
				self.s.close()
				sys.exit()

	def recibir(self):
		print('\nHilo RECIBIR con ID =',threading.currentThread().getName(), '\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		while True:
			try:
				data = self.s.recv(64)
				if data: print(pickle.loads(data)) ##guardo lo que viene del otro lado del recibir, si hay algo, convertir a legible el dato binario
			except: pass

	def enviar(self, msg):
		self.s.send(pickle.dumps(msg)) ##serializar mensaje y enviar

arrancar = Cliente()

		
