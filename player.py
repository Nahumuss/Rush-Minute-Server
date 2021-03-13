import socket
import _socket

class Player(socket.socket):
    def __init__(self, address = '127.0.0.1', id = -1, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.__address = address
        self.__id = id

    def send(self, message):
        if message:
            super().send(message.encode())

    def get_message(self):
        try:
            return self.recv(1024).decode()
        except socket.error:
            self.close()

    @classmethod
    def copy(cls, sock, address = '127.0.0.1', id = -1):
        fd = _socket.dup(sock.fileno())
        copy = cls(sock.family, sock.type, sock.proto, fileno=fd)
        copy.settimeout(sock.gettimeout())
        copy.set_address(address)
        copy.set_id(id)
        return copy

    def set_address(self, address):
        self.__address = address

    def set_id(self, id):
        self.__id = id