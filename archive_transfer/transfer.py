import socket
import tqdm
import os
import argparse

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 512 
HEADER_LENGTH = 10


#funcao para enviar o arquivo 
def send_file(filename, host, port, package_size):
    #Referencia o tamanho do arquivo a ser enviado
    filesize = os.path.getsize(filename)

    #Cria um socket para quem vai enviar o arquivo e conecta a quem recebera
    s = socket.socket()
    print(f"Conectando a {host}:{port}")
    s.connect((host, port))
    print("Conexao estabelecida.")

    #Dependendo da escolha feita anteriormente, define o tamanho dos pacotes a serem enviados
    if package_size == 1:
        BUFFER_SIZE = 512
    elif package_size == 2:
        BUFFER_SIZE = 1024
    elif package_size == 3:
        BUFFER_SIZE = 1536

    #Envia para quem vai receber o arquivo o tamanho a ser trabalhado

    package_string = str(package_size)
    
    #Envia o nome do arquivo e o tamanho
    s.send(f"{package_string}{SEPARATOR}{filename}{SEPARATOR}{filesize}".encode())

    i = 0

    #Envio do arquivo
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=512)
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                #Se nao existem bytes para serem lidos, para
                break
            s.sendall(bytes_read)
            i += 1
            #Atualiza a barra de atualizacao
            progress.update(len(bytes_read))

    print("Total de pacotes enviados:")
    print(i)
    #Fecha o socket
    s.close()



if __name__ == "__main__":
    choice = int(input("1 - Envio de arquivos;\n2 - Recebimento de arquivos;\n"))
    if choice == 1:
        host = input("Insira o IP para o envio de arquivos:")
        port = int(input("Insira o Port:"))
        package_size = int(input("Insira o tamanho dos pacotes a serem enviados:\n1 - 500 bytes;\n2 - 1000 bytes;\n3 - 1500 bytes;\n"))
        filename = input("Insira o arquivo a ser enviado:")
        send_file(filename, host, port, package_size)
       
    elif choice == 2:
        #Endereco e port padroes
        SERVER_HOST = "127.0.0.1"
        SERVER_PORT = 8000

        #Um buffer temporario e setado
        BUFFER_SIZE = 512
        SEPARATOR = "<SEPARATOR>"
        #Cria um socket para quem recebera os arquivos
        s = socket.socket()
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(1)
        print(f"Esperando conexao {SERVER_HOST}:{SERVER_PORT}")
        #Aceita conexao
        client_socket, address = s.accept() 
        #Printa quando ha conexao
        print(f"{address} esta conectado")

        #recebe as informacoes do arquivo, utilizando o socket de quem envia
        received = client_socket.recv(BUFFER_SIZE).decode()
        pack_string,filename, filesize = received.split(SEPARATOR)

        pack_string = int(pack_string)
        if pack_string == 1:
            BUFFER_SIZE = 512
        elif pack_string == 2:
            BUFFER_SIZE = 1024
        elif pack_string == 3:
            BUFFER_SIZE = 1536

        # alteracoes no caminho do arquivo
        filename = os.path.basename(filename)
        filesize = int(filesize)

        # recebe os pacotes e vai reestruturando o arquivo
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=512)
        with open(filename, "wb") as f:
            while True:
                #le o numero de bytes definido no BUFFER SIZE
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:    
                    #finaliza o programa quando nao ha nada a ser lido
                    break
                #escreve os bytes recebidos
                f.write(bytes_read)
                #atualiza a barra de atualizacao
                progress.update(len(bytes_read))

        #fecha o socket de quem enviou
        client_socket.close()
        #fehca o socket do server
        s.close()

    else:
        print("Erro, operacao nao reconhecida")
    