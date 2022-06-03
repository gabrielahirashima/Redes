import socket
import select
import errno
import sys

#define um tamanho para o header que facilita o envio das mensagens
HEADER_LENGTH = 10

IP = input("Insira o IP do servidor:")
PORT = input("Insira o Port:")

#cria um username para o cliente 
meu_usuario = input("Username: ")

#cria um socket para a conexao tcp/ip
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#define o port caso nao passe como input
if not PORT:
    PORT = 1234
else:
    PORT = int(PORT)

#addr sera o endereco para a conexao
ADDR = (IP, PORT)

#conecta o cliente ao servidor addr
client_socket.connect(ADDR)

client_socket.setblocking(False)

#define o username, encodando e somando ao header
usuario = meu_usuario.encode('utf-8')
usuario_header = f"{len(usuario):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(usuario_header + usuario)

while True:

    #enquanto a mensagem nao for enviada, aguarda
    mensagem = input(f'{meu_usuario} > ')

    #se a mensagem nao estiver vazia, 
    if mensagem:

        #encodad a mensagem, a converte e a envia
        mensagem = mensagem.encode('utf-8')
        mensagem_header = f"{len(mensagem):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(mensagem_header + mensagem)

    try:
        #loop para as mensagens enviadas
        while True:

            usuario_header = client_socket.recv(HEADER_LENGTH)

            #sem informacao, o server fecha
            if not len(usuario_header):
                print('Connection closed by the server')
                sys.exit()

            usuario_length = int(usuario_header.decode('utf-8').strip())

            usuario = client_socket.recv(usuario_length).decode('utf-8')

            mensagem_header = client_socket.recv(HEADER_LENGTH)
            mensagem_length = int(mensagem_header.decode('utf-8').strip())
            mensagem = client_socket.recv(mensagem_length).decode('utf-8')

            print(f'{usuario} >>> {mensagem}')

    except IOError as e:
        #Confere se os dados estao chegando corretamente
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        #continua caso apenas nao chegue
        continue

    except Exception as e:
        #cuida de exceptions fora as tratadas acima
        print('Reading error: '.format(str(e)))
        sys.exit()