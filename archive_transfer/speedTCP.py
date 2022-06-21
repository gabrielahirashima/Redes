from email import message_from_binary_file
from multiprocessing import connection
import socket
import os
import time
import select
from traceback import print_tb
import random
import datetime

def main():
    while True:
        print("Escolha uma opcao:")
        op = int(input("1 - Testar upload e download;\n2 - Enviar pacotes de teste;\n"))
        while True:
            if op == 1:
                teste()
                exit()
        
            elif op == 2:
                envio_teste()
                exit()

#**************************************************PARTE SERVIDOR**************************************************#
def upload_s(conexao): #funcao de download no servidor
    stoper = 20
    stop = time.time() + stoper
    while time.time() < stop:
        conexao.recv(1024)
        conexao.send(bytes('1', 'utf8'))

def download_s(conexao): #funcao de envio no servidor
    stoper = 20
    stop = time.time() + stoper
    while time.time() < stop:
        pacote = bytes(bin(random.getrandbits(1024)), 'utf8')
        conexao.send(pacote)

def envio_teste(): #Funciona como se fosse o servidor

    HOST = '127.0.0.1' #HOST e PORT do servidor
    PORT = 8000
    random.seed()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria o socket
    s.bind((HOST, PORT))    #Bind no IP e PORT
    s.listen(1) #Escutando por uma conexao no PORT definido
    print("Aguardando conexao")
    conexao, address = s.accept()
    print("Conexao aceita em: {}" .format(address))

    #---------------------TESTE UPLOAD---------------------#
    conexao.send(bytes('upload', 'utf8')) 
    print("Iniciando teste de upload")
    upload_s(conexao)
    conexao.send(bytes('fim-teste1', 'utf8'))


    time.sleep(1)

    #---------------------TESTE DOWNLOAD---------------------#
    conexao.send(bytes('download', 'utf8')) 
    print("Iniciando teste de download")
    download_s(conexao)
    conexao.send(bytes('fim-teste2', 'utf8'))

    end = connection.recv(5).decode('utf8')

    if not 'fim' in end:
        time.sleep(1)
    
    s.close()

#**************************************************PARTE CLIENTE**************************************************#
def upload_c(s):
   

    tempo_total = time.time()
    #speed = ((bytes*8)/tempo_total)
    #pacotes_seg = pacote_enviados/tempo_total

    #print(f'pacotes por s: {pacotes_seg}\nbytes recebidos: {bytes}\nvelocidade aproximada: {speed}\nerros:{erros}')

def download_c(s):
    bytes = 0
    pacote_enviados = 0
    erros = 0

    inicio = time.time()

    while True:
        try:
            mensagem = s.recv(1024)
            mensagem = mensagem.decode('utf8')
            bytes_rcv  = mensagem.__len__()
            if bytes_rcv == 0:
                erros += 1
            bytes += bytes_rcv
            pacote_enviados += 1
            if 'fim-teste2' in mensagem:
                break
        
        except:
            print("Erro no teste de download!")
            break

    #tempo_total = time.time() - inicio
    #speed = ((bytes*8)/tempo_total)
    #pacotes_seg = pacote_enviados/tempo_total

    #print(f'pacotes por s: {pacotes_seg}\nbytes recebidos: {bytes}\nvelocidade aproximada: {speed}\nerros:{erros}')

def teste():
    HOST = '127.0.0.1'
    PORT = 8000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket criado
    s.connect((HOST, PORT))

    random.seed()

    mensagem = s.recv(4096)
    mensagem = mensagem.decode('utf8')

    if 'upload' in mensagem:
        bytes = 0
        pacote_enviados = 0
        erros = 0

        inicio = time.time()

        while True:
            try:
                mensagem = bytes(bin(random.getrandbits(1024)), 'utf8')
                bytes_sent = s.send(mensagem)
                print("entrous")
                if bytes_sent == 0:
                    erros += 1
                bytes += bytes_sent
                pacote_enviados += 1
                mensagem = s.rcv(20).decode('utf8')
                if 'fim-teste1' in mensagem:
                    break
            
            except:
                print("Erro no teste de upload!")
                exit()
    
    time.sleep(1)

    mensagem = s.recv(4096)
    mensagem = mensagem.decode('utf8')

    if 'download' in mensagem:
        download_c(s)
    
    s.send(bytes('fim', 'utf8'))

if __name__ == "__main__":
    main()