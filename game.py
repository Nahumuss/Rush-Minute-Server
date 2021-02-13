from threading import Thread

class Game:
    def __init__(self, board, player1 = None, player2 = None):
        self.__player1 = player1
        self.__player2 = player2
        self.__board = board

    def game(self):
        pass # TODO game execution

    def start(self):
        game = Thread(target=self.game)
        game.start()

