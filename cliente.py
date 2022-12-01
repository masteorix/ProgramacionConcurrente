#!/usr/bin/env python
# coding: utf-8
import threading
import sys
import socket
import pickle
import os


class Cliente():

    def __init__(self, host=input("Intoduzca la IP del servidor ?  "), port=int(input("Intoduzca el PUERTO del servidor ?  ")), nickname=input("Cual es tu nickname ? ")):
        self.s = socket.socket()
        self.s.connect((host, int(port)))
        print('\n\tProceso con PID = ', os.getpid(), '\n\tHilo PRINCIPAL con ID =', threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ',
              threading.currentThread().isDaemon(), '\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
        threading.Thread(target=self.recibir, daemon=True).start()

        while True:
            msg = input(
                '\nEscriba texto ?   ** Enviar = ENTER   ** Salir Chat = 1 \n')
            with open("u22251035AI1.txt", "a") as f:
                f.write("\n" + nickname + ":" + msg)
                f.close()
            if msg != '1':
                #msg = nickname + ":  " + msg
                self.enviar(msg)
            else:
                print(
                    " **** Me piro vampiro; cierro socket y mato al CLIENTE con PID = ", os.getpid())
                self.s.close()
                sys.exit()

    def sec_mult(self, A, B):
        print("Secuencial:")
        n_fil_A = len(A)  # Obtengo num de filas de A
        print(n_fil_A)
        n_col_A = len(A[0])  # Obtengo num de colunmas de A
        print(n_col_A)
        n_fil_B = len(B)  # Obtengo num de filas de B
        print(n_fil_B)
        n_col_B = len(B[0])
        print(n_col_B)
        if n_col_A != n_fil_B:
            print("Dimension invalida")
        else : 
            # Crear y poblar la matrix  C = A*B
            C = [[0] * n_col_B for i in range(n_fil_A)]
            # Hago la multiplicacion de AxB = C, i para iterar sobre las filas de A
            for i in range(n_fil_A):
                for j in range(n_col_B):  # j para iterar sobre las columnas de B
                    for k in range(n_col_A):  # k para iterar en C
                        # Aqui se hace la multiplicación y guardo en C.
                        C[i][j] += A[i][k] * B[k][j]
            return C
    
    def par_mult(self,A, B):  # f() que prepara el reparto de trabajo para la mult. en paralelo
        import multiprocessing as mp
        import math
        print("Paralelo:")
        # Columnas  a procesar x c/cpre, ver Excel adjunto
        n_fil_A = len(A)  # Obtengo num de filas de A
        print(n_fil_A)
        n_col_A = len(A[0])  # Obtengo num de colunmas de A
        print(n_col_A)
        n_fil_B = len(B)  # Obtengo num de filas de B
        print(n_fil_B)
        n_col_B = len(B[0])
        print(n_col_B)
        n_cores = mp.cpu_count()  # Obtengo los cores de mi pc
        size_col = math.ceil(n_col_B/n_cores)
        # Filas a procesar x c/cpre, ver Excel adjunto
        size_fil = math.ceil(n_fil_A/n_cores)
        # Array MC de memoria compartida donde se almacenaran los resultados, ver excel adjunto
        MC = mp.RawArray('i', n_fil_A * n_col_B)
        cores = []  # Array para guardar los cores y su trabajo
        # Asigno a cada core el trabajo que le toca, ver excel adjunto
        print("heeeey")
        for core in range(n_cores):
            # Calculo i para marcar inicio del trabajo del core en relacion a las filas
            i_MC = min(core * size_fil, n_fil_A)
            # Calculo f para marcar fin del trabajo del core, ver excel
            f_MC = min((core + 1) * size_fil, n_fil_A)
            # Añado al Array los cores y su trabajo
            cores.append(mp.Process(target=self.par_core, args=(A, B, MC, i_MC, f_MC)))
        for core in cores:
            core.start()  # Arranco y ejecuto el trabajo para c/ uno de los cores que tenga mi equipo, ver excel
        for core in cores:
            core.join()  # Bloqueo cualquier llamada hasta que terminen su trabajo todos los cores
        # Convierto el array unidimensional MC en una matrix 2D (C_2D)
        C_2D = [[0] * n_col_B for i in range(n_fil_A)]
        for i in range(n_fil_A):  # i para iterar sobre las filas de A
            for j in range(n_col_B):  # j para iterar sobre las columnas de B
                # Guardo el C_2D los datos del array MC
                C_2D[i][j] = MC[i*n_col_B + j]
        return C_2D


    def par_core(A, B, MC, i_MC, f_MC):  # La tarea que hacen todos los cores
        # Size representado en colores en el excel que itera sobre las filas en A
        for i in range(i_MC, f_MC):
            # Size representado en colores en el excel que itera sobre las columnas en B
            for j in range(len(B[0])):
                for k in range(len(A[0])):  # n_fil_B o lo que es l mismo el n_col_A
                    # Guarda resultado en MC[] de cada core
                    MC[i*len(B[0]) + j] += A[i][k] * B[k][j]

    def recibir(self):

        print('\nHilo RECIBIR con ID =', threading.currentThread().getName(
        ), '\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
        while True:
            try:
                data = self.s.recv(64)
                data1 = pickle.loads(data)
                print(type(data1))
                # data2=np.array(data1)
                # print(data1[1])
                # print("1")
                import random

                # print("2")
                # Genero A[21535220][6]con num. aleatorios del 0 al 215, ver excel
                A = [[random.randint(0, 10) for i in range(data1[1])]for j in range(data1[0])]
                # Genero B[6][21535220]con num. aleatorios del 0 al 215, ver excel
                B = [[random.randint(0, 10) for i in range(data1[2])]for j in range(data1[1])]
                # print("3")
                print(A)
                print(B)
                #matriz_result = self.sec_mult(A, B)

                matriz_result = self.sec_mult(A, B)
                print(matriz_result)
                #matriz_result2 = self.par_mult(A, B)
                #print(matriz_result2)
                '''
                if data:
                    
                    data=pickle.loads(data)
                    print(type(data))
                    data1=int(data)+4
                    print(data1
                    print(data1)
                    print(type(data1))
                    data2=int(data1)
                    print(type(data2
                    try:
                        data1=int(data1)+12
                        print("hola"+type(data1))
                        print(data1)
                    except:
                        print(type(data1))
                        print(data1)
                '''

            except:
                pass

    def enviar(self, msg):
        self.s.send(pickle.dumps(msg))


arrancar = Cliente()
