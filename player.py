import socket
import _socket

class Player(socket.socket):
    def __init__(self, address = '127.0.0.1', id = -1, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.__address = address
        self.__id = id
        self.board = ''

    def send(self, message):
        if message:
            try:
                super().send(message.encode())
            except:
                print("Could not send data")

    def get_message(self):
        try:
            message = self.recv(36)
            if not message:
                raise socket.error
            message = message.replace(b'\x00', b'').decode(encoding='utf-8')
            return message
        except socket.error:
            print("Could not recive data")
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