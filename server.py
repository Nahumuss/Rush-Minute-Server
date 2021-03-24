from player import Player
from game import Game, running_games
from socket import socket
from select import select
from random import randint
from constants import player_amount

with open('levels.txt', 'r') as levels:
    boards = [line[3:39] for line in levels.readlines()]

server_socket = socket()
server_socket.bind(('0.0.0.0', 5635))
server_socket.listen(5)

game_lobby = []

while True:
    rlist, wlist, xlist = select([server_socket] + game_lobby, [], [])
    for current_socket in rlist:
        if current_socket == server_socket:
            (new_socket, address) = server_socket.accept()
            game_lobby.append(Player.copy(new_socket))
            print("Added connection: " + str(address))
        else:
            current_socket.close()
            game_lobby.remove(current_socket)
            print(f"Removed connection: {str(address)} Quit Lobby")
        if len(game_lobby) >= player_amount:
            game = Game(boards[randint(0,999)], game_lobby)
            game.start()
            game_lobby = []