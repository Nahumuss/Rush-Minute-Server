from socket import socket

client_socket = socket()
client_socket.connect(('127.0.0.1', 5635))

while True:
    message = input()
    client_socket.send(message.encode())
    print(client_socket.recv(1024).decode())