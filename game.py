from threading import Thread
from select import select
from constants import win_message, player_amount
from difflib import ndiff

running_games = []

class Game:

    # Creates a new game
    def __init__(self, board, players = []):
        self.__board = board
        self.__pending_messages = []
        for player in players:
            self.__pending_messages.append([f'N;{player.name}', player])
        self.__pending_messages.append([f'U;{self.__board[0]}%{self.__board[1]}', None])
        self.__players = players
        self.__ended = False
        for player in self.__players:
            player.board = self.__board
        running_games.append(self)
        print('Created a game! ' + str(self) + ' with players: ' + str(players))

    # Main loop
    def game(self):
        while self.__players:
            for player in self.__players:
                if player.fileno() == -1:
                    self.__players.remove(player)
                    if len(self.__players) == 1:
                        self.win(self.__players[0], True)
            if self.__players:
                rlist, wlist, _ = select(self.__players, self.__players, self.__players)
                for player in rlist:
                    try:
                        prefix, content = player.get_message()
                    except:
                        print(f'Player {player} disconnected from game {self}')
                        player.close()
                    else:
                        if prefix == 'U' and len(content) == 36 and self.verify_move(player.board, content):
                            player.board[0] = content
                            self.__pending_messages.append([f'{prefix};{content}', player])
                            if content[17] == 'A':
                                self.win(player)
                self.send_pending_messages(wlist)
        else:
            print("Game " + str(self) + " done, players disconnected")
        if not self.__ended:
            self.end([self.__players])

    # Verify a move
    def verify_move(self, old_board, new_board):
        if sorted(old_board[0]) != sorted(new_board):
            return False
        return True

    # Start the game
    def start(self):
        game = Thread(target=self.game)
        try:
            game.start()
        except:
            pass

    # Add a player to the game
    def add_player(self, player):
        if len(self.__players) < player_amount:
            self.__players.append(player)
            return True
        return False

    def end(self, players):
        if not self.__ended:
            self.__ended = True
            if players:
                for player in players:
                    if player:
                        player.send('E;')
                        player.close()
                    self.__players.remove(player)
            running_games.remove(self)

    # Win / send win and lose messages
    def win(self, winner, disconnected = False):
        print(f'Player {winner} from game {self} won!')
        winner.send('W;') if not disconnected else winner.send('D;')
        for loser in [player for player in self.__players if player != winner]:
            loser.send('L;')
        self.end(self.__players)

    # Send the messages waiting to be sent
    def send_pending_messages(self, players):
        for message in self.__pending_messages:
            message_data = message[0]
            sender = message[1]
            for player in players:
                if player != sender:
                    player.send(message_data)
            self.__pending_messages.remove(message)