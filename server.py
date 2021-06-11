from os import remove
from player import Player
from game import Game, running_games
from socket import socket
from select import select
from random import randint
from constants import player_amount
from uuid import uuid4

# Removes a player from the server
def remove_player(player):
    if player in connections:
        connections.remove(player)
    ids = []
    for id in private_lobbies:
        if private_lobbies[id] is player:
            ids.append(id)
    for id in ids:
        private_lobbies.pop(id)

# Removes a player from the main lobby
def remove_from_lobby(player):
    if player in game_lobby:
        game_lobby.remove(player)

if __name__ == '__main__':
    with open('levels.txt', 'r') as levels:
        boards = [[line[3:39]] + [line[0:2]] for line in levels.readlines()] # List of all boards (strings)

        server_socket = socket()
        server_socket.bind(('0.0.0.0', 5635))
        server_socket.listen(5)

        connections = [] # Connected clients
        game_lobby = [] # Main game lobby
        private_lobbies = {} # Private Lobbies

# Main Loop
    while True:
        rlist, _, _ = select([server_socket] + connections, [], [])
        for current_socket in rlist:
            if current_socket is server_socket:
                (new_socket, address) = server_socket.accept()
                connections.append(Player.copy(new_socket, address=address))
                print("Added connection: " + str(address))
            elif current_socket in connections:
                try:
                    prefix, content = current_socket.get_message()
                except:
                    print(f'Player {current_socket} disconncted from lobby')
                    remove_player(current_socket)
                    remove_from_lobby(current_socket)
                else:
                    # Change name
                    if prefix == 'N':
                        current_socket.name = content
                    # Create a private lobby
                    elif prefix == 'C':
                        game_id = str(uuid4())
                        current_socket.send(f'C;{game_id}')
                        private_lobbies[game_id] = current_socket
                    # Join a private lobby / match
                    elif prefix == 'P':
                        if content in private_lobbies and private_lobbies[content] != current_socket:
                            game = Game(boards[randint(0,999)], [current_socket] + [private_lobbies[content]])
                            game.start()
                            remove_player(current_socket)
                            remove_from_lobby(private_lobbies[content])
                            remove_player(private_lobbies[content])
                            remove_from_lobby(current_socket)
                    # Join the main lobby
                    elif prefix == 'R':
                        if not current_socket in game_lobby:
                            game_lobby.append(current_socket)
                            if len(game_lobby) >= player_amount:
                                game = Game(boards[randint(0,999)], game_lobby)
                                for player in game_lobby:
                                    remove_player(player)
                                game_lobby = []
                                game.start()