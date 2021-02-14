from player import Player
from game import Game, running_games
from socket import socket
from select import select
from random import randint

with open('levels.txt', 'r') as levels:
    boards = [line[3:40] for line in levels.readlines()]

server_socket = socket()
server_socket.bind(('0.0.0.0', 80))
server_socket.listen(5)

game_lobby = []

while True:
    rlist, wlist, xlist = select([server_socket], [], [])
    for current_socket in rlist:
        (new_socket, address) = server_socket.accept()
        game_lobby.append(Player.copy(new_socket))
        if len(game_lobby >= 2):
            game = Game(boards[randint(0,1000)], game_lobby)
            game.start()
            game_lobby = []