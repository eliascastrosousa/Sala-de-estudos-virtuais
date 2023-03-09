import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect(('localhost', 8888))

terminado = False
print('Digite tt para encerrar o chat! ')

while not terminado:
    cliente.send(input('Mensagem: ').encode('utf-8'))
    msg = cliente.recv(1024).decode('utf-8')
    if msg == 'tt':
        terminado = True
    else:
        print(msg)

cliente.close