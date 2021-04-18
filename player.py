import socket
import _socket

class Player(socket.socket):
    def __init__(self, address = '127.0.0.1', name = 'Guest', id = -1, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.__address = address
        self.__id = id
        self.name = name
        self.board = ''

    def send(self, message):
        if message:
            try:
                super().send(message.encode())
            except:
                print("Could not send data")

    def get_message(self):
        try:
            message = self.recv(1024)
            if not message:
                return None
            message = message.replace(b'\x00', b'').decode(encoding='utf-8')
            return message.split(';')
        except socket.error:
            print(str(self) + " Disconnected!")
            self.close()
        except:
            print('Error reciving message')

    @classmethod
    def copy(cls, sock, name = 'Guest', address = '127.0.0.1', id = -1):
        fd = _socket.dup(sock.fileno())
        copy = cls(sock.family, sock.type, sock.proto, fileno=fd)
        copy.settimeout(sock.gettimeout())
        copy.set_address(address)
        copy.set_id(id)
        copy.name = name
        return copy

    def set_address(self, address):
        self.__address = address

    def set_id(self, id):
        self.__id = id

    def __str__(self) -> str:
        return f'Username: {self.name}, ip: {self.__address}'

    def __repr__(self) -> str:
        return f'|Username: {self.name}, ip: {self.__address}|'