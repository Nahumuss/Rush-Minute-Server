from threading import Thread
from select import select
from constants import win_message, player_amount
from difflib import ndiff

running_games = []

class Game:

    def __init__(self, board, players = []):
        self.__board = board
        self.__pending_messages = [[self.__board, None]]
        self.__players = players
        for player in self.__players:
            player.board = self.__board
        running_games.append(self)
        print('Created a game! ' + str(self) + ' with players: ' + str(players))

    def game(self):
        while self.__players:
            for player in self.__players:
                if player.fileno() == -1:
                    self.__players.remove(player)
                    break
            if self.__players:
                rlist, wlist, xlist = select(self.__players, self.__players, self.__players)
                if len(self.__players) == 1:
                    self.__pending_messages.append([win_message, None])
                    self.send_pending_messages(wlist)
                    self.__players = None
                for player in rlist:
                    message = player.get_message()
                    if message != None:
                            message = message.replace('$', '')
                            if len(message) == 36:
                                if self.verify_move(player.board, message):
                                    player.board = message
                                    self.__pending_messages.append([message, player])
                                    if message[17] == 'A':
                                        self.win(player)
                self.send_pending_messages(wlist)
        else:
            print("Game " + str(self) + " done, players disconnected")
        self.end([self.__players])

    def verify_move(self, old_board, new_board):
        if sorted(old_board) != sorted(new_board):
            return False
        car_moves = {}
        if new_board == self.__board:
            return True
        for i in range(len(old_board)):
            new_tile = new_board[i]
            old_tile = old_board[i]
            if new_tile != old_tile:
                if (new_tile != 'o' and old_tile != 'o') or (new_tile == 'x' or old_tile == 'x'):
                    return False
                if new_tile == 'o':
                    car = new_tile
                    car_moves.get(car,[0,0])[0] += 1
                else:
                    car = old_tile
                    car_moves.get(car,[0,0])[1] += 1
        for car in car_moves:
            if car[0] != car[1]:
                return False
        return True


    def start(self):
        game = Thread(target=self.game)
        try:
            game.start()
        except:
            pass

    def add_player(self, player):
        if len(self.__players) < player_amount:
            self.__players.append(player)
            return True
        return False

    def end(self, players):
        if players:
            for player in players:
                if player:
                    player.send('end')
                    player.close()
            running_games.remove(self)

    def win(self, winner):
        print(f'Player {winner} from game {self} won!')
        winner.send('whyareyoutryingtocheat/readmycodebro')
        for loser in [player for player in self.__players if player != winner]:
            loser.send('lmfaololyoulostthatonerealhardgonext')
        self.end(self.__players)

    def send_pending_messages(self, players):
        for message in self.__pending_messages:
            message_data = message[0]
            sender = message[1]
            for player in players:
                if player != sender:
                    player.send(message_data)
            self.__pending_messages.remove(message)