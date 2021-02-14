from socket import socket

client_socket = socket()
client_socket.connect(('127.0.0.1', 80))

while True:
    client_socket.send(input().encode())
    print(client_socket.recv(1024).decode)