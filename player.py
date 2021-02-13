from socket import socket

class Player(socket):
    def __init__(self, socket, id):
        self.__socket = socket
        self.__id = id

    def send(self, message):
        self.__socket.send(message.encode())

    def get_message(self):
        self.__socket.recv(1024).decode()
