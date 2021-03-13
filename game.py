from threading import Thread
from select import select
from constants import win_message, player_amount

running_games = []

class Game:

    def __init__(self, board, players = []):
        self.__board = board
        self.__pending_messages = [self.__board]
        self.__players = players
        running_games.append(self)
        print('Created a game!')

    def game(self):
        while True:
            if self.__players:
                for player in self.__players:
                    if player.fileno() == -1:
                        self.__players.remove(player)
            if self.__players:
                rlist, wlist, xlist = select(self.__players, self.__players, self.__players)
                if len(self.__players) == 1:
                    self.__pending_messages.append(win_message)
                    self.send_pending_messages(wlist)
                    self.__players = None
                messages = [player.get_message() for player in rlist]
                for message in messages:
                    if message != None:
                        if message == 'notdone': # TODO
                            self.end(wlist)
                        self.__pending_messages.append(message)
                self.send_pending_messages(wlist)
            else:
                break
        print("Game " + str(self) + " done")
        self.end([])

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
        for player in players:
            player.send('end')
            player.close()
        running_games.remove(self)

    def send_pending_messages(self, players):
        for message in self.__pending_messages:
            print("Sending: " + str(message))
            for player in players:
                player.send(message)
            self.__pending_messages.remove(message)