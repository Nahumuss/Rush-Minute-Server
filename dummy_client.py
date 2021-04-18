from socket import socket
import threading

def read():
    while True:
        message = client_socket.recv(1024)
        if not message:
            break
        print(message.decode())

client_socket = socket()
client_socket.connect(('127.0.0.1', 5635))
t = threading.Thread(target=read)
t.start()

while True:
    message = input()
    client_socket.send(message.encode())