import time
import socket
import random
from traceback import print_tb

#---------------------------------------------------------- MAIN -------------------------------------------------------------------#
while True:
    IP_S = '169.254.189.186'
    PORT_S = 8000
    IP_C = '127.0.0.1'
    PORT_C = 8000
    teste = "teste de rede *2022*"
    msgsize = len(teste)
    testmessage = ''
    for i in range(0, 500, msgsize):
       testmessage = testmessage + teste
        
    print("Escolha uma opcao:")
    op = int(input("1 - Testar upload e download;\n2 - Enviar pacotes de teste;\n"))
    
    while True:
        #Lado "cliente"
        if op == 1:
                #Criacao e conexao ao servidor
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((IP_S, PORT_S))
                stop = 20
                
                bytes_enviados = 0
                pacotes = 0
                            
                s.send(bytes('upload', 'utf8'))
                print('\nIniciando teste de upload...')
                start_upload = time.time()
                
                while time.time() < start_upload+stop:
                    try:
                        msg = bytes((testmessage), 'utf8')
                        envio = s.send((msg))
                        bytes_enviados += envio 
                        pacotes += 1
                                
                    except:
                        print("Erro em teste de upload")
                        break
                
                s.send(bytes('fim-teste-upload', 'utf8'))
                
                time.sleep(1)
                
                s.send(bytes(f'{pacotes}', 'utf8'))
                
                
                bits_enviados = bytes_enviados * 8
                pacotes_segundo = pacotes/20
                velocidade_upload = (bits_enviados)/20
                
                print(f'\nTotal de pacotes enviados: {pacotes}' )
                print(f'Pacotes enviados por segundo{pacotes_segundo}')
                print(f'Total de bits enviados: {bits_enviados}\nBits enviados: {"{:,}".format(bits_enviados)}')
                print(f'Velocidade media(Bits/s): {"{:,}".format(velocidade_upload)}\nVelocidade media(KBits/s):{"{:,}".format(velocidade_upload/(2**10))}')
                print(f'Velocidade media(MBits/s):{"{:,}".format(velocidade_upload/(2**20))}\nVelocidade media(GBits/s):{"{:,}".format(velocidade_upload/(2**30))}')
                print(f'Mbits enviados: {"{:,}".format(bits_enviados/(2**20))}\nTamanho do header:20 bytes/160 bits')
                
                print('\nFim teste de upload...')
                
                s.send(bytes('fim-testes', 'utf8'))
                    
                s.close()
                exit()
        

          
        
    #Lado "servidor"
        elif op == 2:
            pacotes = 0
            stop = 20
            #Criacao e definicao de socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((IP_S, PORT_S))
            s.listen(1)
            print("Aguardando conexao...")

            conexao, address = s.accept()
            print("Conexao aceita em: {}" .format(address))

            #TESTE DE UPLOAD
            bytes_recebidos = 0
            pacotes_upload = 0
            
            msg = conexao.recv(500)
            msg = msg.decode('utf8')

            if 'upload' in msg:
                print('\nIniciando teste de download...')
                start_upload = time.time()

                while True:
                    try:
                        msg = conexao.recv(500)
                        msg = msg.decode('utf8')
                        bytes_received = msg.__len__()
                        bytes_recebidos += bytes_received
                        if(bytes_received == 500):
                            pacotes_upload += 1
                        if 'fim-teste-upload' in msg:
                            print("Fim do teste de download")
                            break

                    except:
                        print("Erro em teste de upload")
                        break
                
            
                tempo_total = time.time() - start_upload
                bits_recebidos = bytes_recebidos*8
                velocidade = (bits_recebidos)/tempo_total
                
                msg = conexao.recv(50).decode('utf8')
                pacotes_enviados = int(msg)
                pacotes_perdidos = pacotes_enviados - pacotes_upload
                pacotes_segundo = pacotes_upload/20

                print(f'Total de pacotes recebidos: {pacotes_upload}\nTotal de pacotes enviados: {pacotes_enviados}')
                print(f'Pacotes recebidos por segundo: {pacotes_segundo}')
                print(f'Total de pacotes perdidos: {pacotes_perdidos}\nTempo Decorrido: {tempo_total}s\nTotal de bits recebidos: {bits_recebidos}\nBits recebidos: {"{:,}".format(bytes_recebidos*8)}')
                print(f'Velocidade media(Bits/s): {"{:,}".format(velocidade)}\nVelocidade media(KBits/s):{"{:,}".format(velocidade/(2**10))}')
                print(f'Velocidade media(MBits/s):{"{:,}".format(velocidade/(2**20))}\nVelocidade media(GBits/s):{"{:,}".format(velocidade/(2**30))}')
                print(f'Mbits recebidos: {"{:,}".format(bits_recebidos/(2**20))}\nTamanho do header:20 bytes/160 bits')
 
            end = conexao.recv(1024).decode('utf8')
            if not 'fim-testes' in end:
                time.sleep(1)
            print("\nFim dos testes")
            
            conexao.close()
            s.close()
            exit()
  