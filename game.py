from threading import Thread
from select import select
from constants import win_message, player_amount

running_games = []

class Game:

    def __init__(self, board, players = []):
        self.__board = board
        self.__pending_messages = [[self.__board, None]]
        self.__players = players
        running_games.append(self)
        print('Created a game! ' + str(self) + ' with players: ' + str(players))

    def game(self):
        while self.__players:
            for player in self.__players:
                if player.fileno() == -1:
                    self.__players.remove(player)
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
                                self.__pending_messages.append([message, player])
                self.send_pending_messages(wlist)
        else:
            print("Game " + str(self) + " done, players disconnected")
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
            message_data = message[0]
            sender = message[1]
            for player in players:
                if player != sender:
                    player.send(message_data)
            self.__pending_messages.remove(message)