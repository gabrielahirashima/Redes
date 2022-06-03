import time
import socket
import random
import select
from traceback import print_tb




#---------------------------------------------------------- MAIN -------------------------------------------------------------------#
def teste(op):
    IP_S = '169.254.189.186'
    PORT_S = 8000
    IP_C = '127.0.0.1'
    PORT_C = 8000
    teste = "teste de rede *2022*"
    msgsize = len(teste)
    testmessage = ''
    for i in range(0, 500, msgsize):
       testmessage = testmessage + teste
    
    #Lado emissor
    if op == 1:
        #Criacao de socket que envia dados
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes_enviados = 0
        pacotes = 0
        print('\nIniciando teste de upload...')
        s.sendto(bytes('teste-upload', 'utf8'), (IP_S, PORT_S)) #notifica início do envio
        inicio = time.time()
        while time.time() < inicio+20:
            try:
                bytes_sent = s.sendto(bytes(testmessage, 'utf-8'), (IP_S, PORT_S))
                bytes_enviados += bytes_sent
                pacotes += 1

            except:
                print("\nErro em teste de upload")      #notifica algo errado no geral e interrompe
                break
            
        s.sendto(bytes('fim-teste-upload', 'utf8'), (IP_S, PORT_S)) #notifica o fim do envio
        s.sendto(bytes(str(pacotes), 'utf-8'), (IP_S, PORT_S))      #envia o número de pacotes enviados
        print("\nFim do teste de upload")
        tempo_total = time.time() - inicio
        velocidade = bytes_enviados/tempo_total
        velocidade_uploadP = pacotes/tempo_total

        print(f'\nTotal de pacotes enviados: {"{:,}".format(pacotes)}\nTempo Decorrido: {tempo_total}s\nBits enviados: {"{:,}".format(bytes_enviados*8)}\nVelocidade media(bits/s): {"{:,}".format(velocidade*8)}\nVelocidade media(kbits/s): {"{:,}".format((velocidade/2**10)*8)}\nVelocidade media(Mbits/s): {"{:,}".format((velocidade/2**20)*8)}\nVelocidade media(Gbits/s): {"{:,}".format((velocidade/2**30)*8)}\nVelocidade media(pacotes/s):{"{:,}".format(velocidade_uploadP)}')
        s.close()

        #Lado receptor
    elif op == 2:
            #Criacao e definicao de socket receptor
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((IP_S, PORT_S))
            print("\nAguardando...")
            s.settimeout(60) #timeout caso demore para receber/nenhum dado chegue

            bytes_recebidos = 0
            pacotes_download = 0
            msg, address = s.recvfrom(500)
            msg = msg.decode('utf-8')
            if 'teste-upload' in msg:
                print('\nIniciando teste de download...')
                inicio_download = time.time()
                while True:
                    try:
                        s.setblocking(False)
                        ready = select.select([s],[],[],15)

                        if ready[0]:
                            msg, address = s.recvfrom(500)     #timeout
                        else: print("erro")
                        
                        msg = msg.decode('utf8')
                        bytes_received = len(msg)
                        bytes_recebidos += bytes_received
                        if bytes_received == 500:
                            pacotes_download += 1
                        #if not msg:
                            #break                               
                        if 'fim-teste-upload' in msg:           #confirmações de final
                            print("\nFim do teste de download")
                            break

                    except:
                        print("\nErro em teste de download")        #notifica algo errado no geral e interrompe
                        break
                try:
                    s.setblocking(False)
                    ready = select.select([s],[],[],15)

                    if ready[0]:
                       pc, address = s.recvfrom(500)      #timeout
                    else: print("erro")
                    
                    pacotes_upload = pc.decode('utf-8')
                    tempo_total_download = time.time() - inicio_download
                    velocidade_download = bytes_recebidos/tempo_total_download
                    velocidade_downloadP = pacotes_download/tempo_total_download
                    lost = int(pacotes_upload) - pacotes_download       #pacotes perdidos
                    
                    if lost < 0:        #acontece de contabilizar 1 pacote enviado a mais em casos de envio ótimos (-1 perdidos), para isso retificamos para 0
                        lost = 0
                    print(f'\nTotal de pacotes recebidos: {"{:,}".format(pacotes_download)}\nTempo Decorrido: {tempo_total_download}s\nBits recebidos: {"{:,}".format(bytes_recebidos*8)}\nVelocidade média(bits/s): {"{:,}".format(velocidade_download*8)}\nVelocidade média(kbits/s): {"{:,}".format((velocidade_download/2**10)*8)}\nVelocidade média(Mbits/s): {"{:,}".format((velocidade_download/2**20)*8)}\nVelocidade média(Gbits/s): {"{:,}".format((velocidade_download/2**30)*8)}\nVelocidade media(pacotes/s): {"{:,}".format(velocidade_downloadP)}')
                    print(f'\nPacotes perdidos: {"{:,}".format(lost)}\nTamanho de pacote: 520 bytes\nCabeçalho: 20 bytes  Payload: 500 bytes')
                except:
                    if pc == None:
                        print("string nula")     #exceção que acontece em caso de bytes nulos/vazios que atrapalham ao receber informações
            
            else: print('Nenhum dado recebido.')

            print("\nFim dos testes")
            s.close()

    elif op == 3: #Encerrar o programa
            exit()

def main():
     while True:
        print("\nEscolha uma opcao:")
        option = int(input("1 - Enviar pacotes de teste;\n2 - Receber pacotes de teste;\n3 - Sair.\n"))
        teste(option)

main()