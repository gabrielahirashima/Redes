import socket
import os
import time
import select

class FileTransferer:
    def __init__(self, host_ip, host_port, local_ip, local_port):
        # settings of the file
        self.separator = "<SEPARATOR>"
        self.buffer_size = 1024

        # ip and port settings
        self.host_ip = host_ip
        self.host_port = host_port
        self.local_ip = local_ip
        self.local_ip = local_port

        self.conn_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        # menu 
        while True:
            print("Iniciando programa....")
            while True:
                self.buffer_size = int(input("Insira o tamanho dos pacotes a serem trabalhados (500, 1000 ou 1500):"))
                if (self.buffer_size == 500) or (self.buffer_size == 1000) or (self.buffer_size == 1500):
                    break
                print("Tamanho invalido.")

            while True:
                print("Escolha uma opcao:")
                op = int(input("1 - Envio de arquivos;\n2 - Recebimento de arquivos;\n"))
                while True:
                    if op == 1:
                        self.host_ip = input("Insira o IP de quem recebera o arquivo:")
                        self.host_port = int(input("Insira o PORT de quem recebera o arquivo:"))
                        filepath = input("Insira o arquivo a ser enviado:")
                        self.sendFile(filepath)
                        exit()
                      
                    if op == 2:
                        self.local_ip = input("Insira o seu IP:")
                        self.local_port = int(input("Insira o seu PORT:"))
                        self.receiveFile()
                        exit()

                    else:
                        print("Formato invalido")

        
    def sendFile(self, filepath):
        self.conn_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr = (self.host_ip, self.host_port)

        filesize = os.path.getsize(filepath)
        self.conn_socket.sendto(str(os.path.basename(filepath)).encode('ascii'), addr)
        print(f"Enviando dados a {self.host_ip}:{self.host_port}....")
        time.sleep(0.5)
        print("Dados enviados.")

        self.conn_socket.sendto(str(filesize).encode('ascii'), addr)
        time.sleep(0.5)

        with open(filepath, "rb") as f:
            start = time.time()
            aux = 0
            bytes_read = f.read(self.buffer_size)
            while (bytes_read):
                if self.conn_socket.sendto(bytes_read, addr):
                    bytes_read = f.read(self.buffer_size)
                    aux += 1
                    if aux == 2:
                        time.sleep(0.02)
                        aux = 0

            print("Tamanho do arquivo original: ", filesize , " bytes")            
            print("Tamanho do arquivo: ", f.tell(), " bytes")
            print("Numero de pacotes enviados: ", f.tell() // self.buffer_size + 1)
        self.conn_socket.close()
        print("Arquivo enviado.")

    def receiveFile(self):
        self.conn_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        timeout = 3
        print("Aguardando dados...")
        self.conn_socket.bind((self.local_ip, self.local_port))
  
        data, addr = self.conn_socket.recvfrom(1024)
        print(f"Dados de {addr} recebidos")
        filepath = ''
        filesize = 0
        if data:
            filepath = data.decode('ascii')
            print(f"Arquivo: {filepath}")

        data, addr = self.conn_socket.recvfrom(5)
        filesize = int(data.decode('ascii'))

        f = open(filepath, "wb")
        start = time.time()
        while True:
        # read the bytes (size of buffer_size) from the socket (receive)
            ready = select.select([self.conn_socket], [], [], timeout)
            if ready[0]:
                data, addr = self.conn_socket.recvfrom(self.buffer_size)
                f.write(data)
            else:
                break

        print("Tamanho do arquivo:", f.tell(), "bytes")
        print("Numero de pacotes recebidos: ", f.tell() // self.buffer_size + 1)
        f.close()
        self.conn_socket.close()
        print("Arquivo recebido")


fileTransferer = FileTransferer('192.168.0.1', 5001, '192.168.0.1', 5002)
fileTransferer.start()