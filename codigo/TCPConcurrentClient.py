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
