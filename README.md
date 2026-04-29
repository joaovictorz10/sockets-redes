# Resumo prático: Sockets TCP e UDP

Este repositório contém a implementação e os testes dos códigos fornecidos na atividade referente ao slide `REDES3_ES_TCP_Sockets_Parte2.pdf`.

> **Nota sobre a execução:** Os códigos dos clientes foram adaptados conforme a instrução da atividade, alterando o endereço/nome do servidor para `127.0.0.1` (localhost) para possibilitar a execução e teste na própria máquina local.

Abaixo é apresentado o relatório detalhado, contendo o código-fonte, uma explicação de funcionamento e o registro da saída (captura) de cada par Cliente/Servidor testado.

---

## 1. Sockets UDP (User Datagram Protocol)

O UDP é um protocolo de transporte sem conexão, focado no envio rápido de pacotes (datagramas), mas não garante a entrega confiável. Em vez de estabelecer uma conexão prévia, o cliente simplesmente empacota os dados com o endereço de destino e os envia.

### Código do Servidor (`UDPServer.py`)
```python
from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('The server is ready to receive')

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
```

### Código do Cliente (`UDPClient.py`)
```python
from socket import *

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('Input lowercase sentence: ')
clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()
```

### Explicação do Funcionamento
1. O **Servidor UDP** inicializa um socket vinculado à porta `12000` na própria máquina e entra em um laço infinito aguardando o recebimento de mensagens através da função `recvfrom()`.
2. O **Cliente UDP** solicita uma entrada de texto do usuário (em minúsculas), formata e a envia ao servidor especificando o IP `127.0.0.1` e a porta `12000` via `sendto()`. Ele então espera por um pacote de resposta.
3. Ao receber o pacote do cliente, o servidor extrai o conteúdo da mensagem e o endereço de quem enviou. Ele decodifica a string, a converte inteiramente para maiúsculas (`.upper()`), e devolve a resposta para o endereço de origem, usando a mesma porta em que escuta.
4. O cliente recebe a resposta, imprime-a e encerra a execução com `close()`.

### Captura de Saída (Execução)

**Terminal do Servidor:**
```text
The server is ready to receive
```

**Terminal do Cliente:**
```text
Input lowercase sentence: redes de computadores
REDES DE COMPUTADORES
```

---

## 2. Sockets TCP (Transmission Control Protocol) Simples

O TCP é um protocolo orientado à conexão e confiável. Antes de começar a trocar dados, uma conexão direta (um "handshake") precisa ser estabelecida entre o cliente e o servidor.

### Código do Servidor (`TCPServer.py`)
```python
from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()
```

### Código do Cliente (`TCPClient.py`)
```python
from socket import *

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = input('Input lowercase sentence: ')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('From Server:', modifiedSentence.decode())
clientSocket.close()
```

### Explicação do Funcionamento
1. O **Servidor TCP** cria o socket e o vincula à porta `12000`. Depois ele inicia o modo escuta `listen(1)`. Dentro do laço infinito, a função `accept()` trava e aguarda o pedido de conexão de um novo cliente, criando um socket de comunicação isolado (`connectionSocket`) unicamente para lidar com aquele cliente assim que ele se conectar.
2. O **Cliente TCP** inicializa seu socket e usa `connect()` para efetuar um handshake (conexão) formal com o IP `127.0.0.1` e a porta `12000`.
3. Uma vez conectado, o cliente solicita uma entrada, codifica a mensagem e a transmite usando um simples `.send()`, sem precisar especificar o destino de cada pacote (pois a conexão TCP já detém essa informação).
4. O servidor recebe a mensagem por meio da conexão específica, processa convertendo o texto para maiúsculas, envia a resposta de volta e imediatamente encerra a conexão para esse cliente (`connectionSocket.close()`).
5. O cliente finalmente recebe, exibe a saída que foi formatada com "From Server: " e fecha seu próprio lado da conexão.

### Captura de Saída (Execução)

**Terminal do Servidor:**
```text
The server is ready to receive
```

**Terminal do Cliente:**
```text
Input lowercase sentence: teste conexao tcp
From Server: TESTE CONEXAO TCP
```

---

## 3. Servidor TCP Concorrente (Multithread)

No modelo anterior, o servidor atende a um cliente, recebe uma única mensagem, fecha a conexão e volta a esperar pelo próximo. Em um modelo **TCP Concorrente** (Multithread), o servidor é capaz de manter a comunicação em aberto simultaneamente com múltiplos clientes, delegando o atendimento a Threads em paralelo.

### Código do Servidor (`TCPConcurrentServer.py`)
```python
# -*- coding: utf-8 -*-
"""
Exemplo de um Servidor TCP Concorrente (Multithread)
Artigo: https://www.linkedin.com/pulse/python-sockets-criando-um-servidor-tcp-concorrente-diego/
Diego Mendes Rodrigues
"""

import socket
import _thread

HOST = '127.0.0.1'
PORT = 50000

def conectado(con, cliente):
    print('\nCliente conectado:', cliente)
    while True:
        msg = con.recv(1024)
        if not msg:
            break
        print('\nCliente..:', cliente)
        print('Mensagem.:', msg.decode())
    print('\nFinalizando conexao do cliente', cliente)
    con.close()
    _thread.exit()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)
print('\nServidor TCP concorrente iniciado no IP', HOST, 'na porta', PORT)

while True:
    con, cliente = tcp.accept()
    print('\nNova thread iniciada para essa conexao')
    _thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
```

### Código do Cliente (`TCPConcurrentClient.py`)
```python
import socket

HOST = '127.0.0.1'
PORT = 50000

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
destino = (HOST, PORT)
tcp.connect(destino)

print('\nDigite suas mensagens')
print('Para sair use CTRL+X\n')

try:
    mensagem = input()
    while mensagem != '\x18':
        tcp.send(str(mensagem).encode())
        mensagem = input()
except EOFError:
    pass

tcp.close()
```

### Explicação do Funcionamento
1. O **Servidor TCP Concorrente** aguarda conexões na porta `50000`. Quando o `accept()` é disparado e retorna um socket de conexão, em vez de processar o cliente em sua thread principal (o que bloquearia a recepção de novos clientes), o servidor importa o módulo `_thread` e delega a conexão a uma nova thread chamando a função em background `conectado()`.
2. O **Cliente Concorrente** conecta-se de forma idêntica ao TCP simples. No entanto, ele agora implementa um laço `while` interativo. O usuário pode continuar digitando mensagens seguidas (como um chat).
3. A função disparada na Thread isolada do servidor recebe essas múltiplas mensagens e imprime na tela do servidor acompanhado do IP/Porta do cliente gerador.
4. Quando o cliente informa o caractere especial ativado pela combinação de teclas de escape `CTRL+X` (`\x18`), o cliente quebra seu laço de `input` e fechará sua ponta do socket.
5. No lado do servidor, quando o cliente finaliza o TCP e não tem mais mensagens para enviar (`if not msg:`), o loop de leitura da thread chega ao fim e a thread é finalizada sem afetar o servidor principal nem outros clientes que estejam ativos em outras threads.

### Captura de Saída (Execução)

**Terminal do Servidor:**
```text
Servidor TCP concorrente iniciado no IP 127.0.0.1 na porta 50000

Nova thread iniciada para essa conexao

Cliente conectado: ('127.0.0.1', 52341)

Cliente..: ('127.0.0.1', 52341)
Mensagem.: Ola Servidor TCP!

Cliente..: ('127.0.0.1', 52341)
Mensagem.: Essa e uma segunda mensagem

Finalizando conexao do cliente ('127.0.0.1', 52341)
```

**Terminal do Cliente:**
```text
Digite suas mensagens
Para sair use CTRL+X

Ola Servidor TCP!
Essa e uma segunda mensagem
```
*(Nota: O cliente aguarda `CTRL+X` antes de encerrar o processo).*
