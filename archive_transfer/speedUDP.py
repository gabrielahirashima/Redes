from multiprocessing import connection
import socket
import os
import time
import select
from traceback import print_tb

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def main():
    while True:
        print("Escolha uma opcao:")
        op = int(input("1 - Receber arquivos;\n2 - Enviar arquivos;\n"))
        
        while True:
            if op == 1:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                pacotes = 0

                s.connect(('127.0.0.1', 8000))
                print('Conectado ')

                nomeArquivo = str(input('Arquivo que deseja receber: '))

                s.send(nomeArquivo.encode())    
                
                start = time.time()
                stop_second = 20
                while time.time() - start < stop_second:
                    while 1:
                        data = s.recv(1024)
                        if not data:
                            break
                        pacotes += 1
                
                print(f"O total de pacotes recebidos em 20s foi: {pacotes}")
                print("O tamanho do arquivo e de " +str(pacotes*1024))
                print("O download medio foi de " + str(pacotes/20) + " bytes por segundo")

                exit()
                
            if op == 2:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                host_ip = "127.0.0.1"
                host_port = 8000
                addr = (host_ip, host_port)
                s.listen(1)
                print('Aguardando pedido de arquivo...')  
                connection, address = s.accept()
                print('Pedido Aceito')  
                nomeArquivo = connection.recv(1024).decode()
                pacotes = 0 

                with open(nomeArquivo, "rb") as file:
                    start = time.time()
                    stop_second = 20
                    while time.time() - start < stop_second:
                        bytes_read = file.read(1024)    
                        while 1:
                            if connection.send(bytes_read):
                                bytes_read = file.read(1024)
                                pacotes += 1
                            if not bytes_read:
                                break

                print('Arquivo Enviado')
                print(f"O total de pacotes enviados em 20s foi: {pacotes}")
                print("O tamanho do arquivo enviado foi " +str(pacotes*1024))
                print("O upload medio foi de " + str(pacotes/20) + " bytes por segundo")                
                exit()
            

if __name__ == "__main__":
    main()