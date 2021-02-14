from threading import Thread
from select import select

class Game:
    def __init__(self, board, players = []):
        self.__pending_messages = []
        self.__players = players
        self.__board = board

    def game(self):
        while True:
            rlist, wlist, xlist = select(self.__players, self.__players, self.__players)
            messages = [player.get_message() for player in rlist]
            for message in messages:
                print(message)
                self.__pending_messages.append(message)
            self.send_pending_messages(wlist)

    def start(self):
        game = Thread(target=self.game)
        game.start()

    def add_player(self, player):
        if len(self.__players) < 2:
            self.__players.append(player)
            return True
        return False

    def send_pending_messages(self, players):
        for message in self.__pending_messages:
            for player in players:
                player.send(message)




