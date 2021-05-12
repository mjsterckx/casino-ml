from blackjack.blackjack import *


class Player:
    balance = 0
    player_id = 0
    wins = 0
    losses = 0

    def __init__(self, player_id, balance=1000):
        self.balance = balance
        self.player_id = player_id

    def win(self, amount):
        self.wins += 1
        self.balance += amount

    def lose(self, amount):
        self.losses += 1
        self.balance -= amount


table = BlackjackTable(n_decks=4)
player_1 = Player(1)
player_2 = Player(2)
player_3 = Player(3)
table.add_player(player_1)
#table.add_player(player_2)
#table.add_player(player_3)
for _ in range(1000):
    table.play()
print('Player 1 balance: ' + str(player_1.balance) + '; wins: ' + str(player_1.wins) + '; losses: ' + str(player_1.losses))
#print('Player 2 balance: ' + str(player_2.balance) + '; wins: ' + str(player_2.wins) + '; losses: ' + str(player_2.losses))
#print('Player 3 balance: ' + str(player_3.balance) + '; wins: ' + str(player_3.wins) + '; losses: ' + str(player_3.losses))
