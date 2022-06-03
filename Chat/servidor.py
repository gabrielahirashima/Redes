import socket
import select #o módulo select permite operar dados em nível de sistema operacional, bem útil para casos como monitorar várias conexões simultaneamente.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #permite o socket a reutilizar o mesmo endereço
s.bind(("127.0.0.1", 8000)) #define o socket para ser porta de entrada do IP desta máquina e do port atribuído
s.listen() #aceita conexões

slist = [s] #lista de sockets, para select monitorar

clientes = {} #dicionário de clientes


def receber_msg(c): #função que recebe mensagens
    try:
        msg_cabec = c.recv(10) #ler o cabeçalho

        if not len(msg_cabec): #lidar com encerramento de conexão
            return False
        
        msg_tam = int(msg_cabec.decode("utf-8")) #converter o cabeçalho para seu comprimento
        return {"cabecalho": msg_cabec, "dados": c.recv(msg_tam)} #dados retornados: cabeçalho e tamanho da mensagem

    except: #alguma coisa deu errado (cliente forçou saída, mensagem vazia...)
        return False


while True:
    reads, _, exceptions = select.select(slist, [], slist) #select para organizar listas de soquetes de clientes. (leitura de lista, escrita de lista, lista de erros respectivamente.) Retorna os mesmos três elementos parâmetros como subconjuntos deles mesmos (uma lista de soquetes prontos para uso)

    for news in reads: #loop que vai iterar sobre a lista de sockets com dados para serem lidos (mensagens)
        if news == s: #se o soquete notificado é o servidor, temos uma conexão nova para lidar
            c, endereco_cliente = s.accept() #aceita a conexão nova recebendo o objeto de socket cliente e seu endereço

            usuario = receber_msg(c) #armazena o nome de usuario que o cliente escolher
            if usuario is False: #se nada acontecer, seguir em frente
                continue

            slist.append(c) #adiciona o novo soquete para a lista de soquetes

            clientes[c] = usuario #armazenar o nome de usuario como a chave para seu respectivo objeto socket

            print(f"conexão de {endereco_cliente[0]}:{endereco_cliente[1]} nome:{usuario['dados'].decode('utf-8')} aceita.")

        else: #se o soquete notificado não é do servidor, há uma mensagem para ser lida
            msg = receber_msg(news)

            if msg is False: #verifica se a mensagem existe. Se o cliente desconecta, a mensagem estaria vazia
                print(f"conexao de {clientes[news]['dados'].decode('utf-8')}")
                slist.remove(news)
                del clientes[news]
                continue

            usuario = clientes[news] #armazenar a informação caso não houve desconexão
            print(f"mensagem recebida de {usuario['dados'].decode('utf-8')}: {msg['dados'].decode('utf-8')}")

            for c in clientes: #itera pela lista de clientes enviando a mensagem para cada um
                if c != news:
                    c.send(usuario['cabecalho'] + usuario['dados'] + msg['cabecalho'] + msg['dados'])

    for news in exceptions: #lidar com soquetes resultantes em exceções e erros
        slist.remove(news)
        del clientes[news]