from blackjack.blackjack import *


class Player:
    balance = 0
    player_id = 0

    def __init__(self, player_id, balance=1000):
        self.balance = balance
        self.player_id = player_id


table = BlackjackTable(n_decks=4)
player_1 = Player(1)
player_2 = Player(2)
player_3 = Player(3)
table.add_player(player_1)
table.add_player(player_2)
table.add_player(player_3)
table.play()
