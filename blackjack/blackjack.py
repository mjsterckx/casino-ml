import random


class BlackjackPlayer:
    table = None
    hands = None
    player = None
    dealer = False

    def __init__(self, table, player, dealer=False):
        self.table = table
        self.player = player
        self.dealer = dealer
        self.reset_hands()

    def add_card(self, hand, card):
        self.hands[hand].append(card)

    def reset_hands(self):
        self.hands = [[], []]

    def score(self, hand):
        score = 0
        aces = 0
        for i in self.hands[hand]:
            if i in ['K', 'Q', 'J']:
                score += 10
            elif i == 'A':
                score += 11
                aces += 1
            else:
                score += int(i)
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
        return score

    def play(self):
        score = self.score(0)
        limit = 21
        if self.dealer:
            limit = 17
        while score < limit:
            self.add_card(0, self.table.hit())
            score = self.score(0)


class BlackjackTable:
    n_decks = 0
    cards = []
    players = []

    def __init__(self, n_decks=4):
        self.n_decks = n_decks
        self.reset_table()

    def reset_table(self):
        cards = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
        for d in range(self.n_decks * 4):
            for c in cards:
                self.cards.append(c)
        random.shuffle(self.cards)

    def add_player(self, player):
        self.players.append(BlackjackPlayer(self, player))

    def remove_player(self, player):
        for p in range(len(self.players)):
            if self.players[p].player_id == player.player_id:
                self.players.pop(p)

    def hit(self):
        card = self.cards[0]
        self.cards.pop(0)
        return card

    def deal(self):
        for i in range(2):
            for p in self.players:
                p.add_card(0, self.hit())

    def play(self):
        self.players.append(BlackjackPlayer(self, None, dealer=True))
        self.deal()
        for p in self.players:
            p.play()
            if not p.dealer:
                print('Player ' + str(p.player.player_id) + ': ' + str(p.hands[0]) + '; score: ' + str(p.score(0)))
            else:
                print('Dealer: ' + str(p.hands[0]) + '; score: ' + str(p.score(0)))
            p.reset_hands()
        self.players.pop()
        if len(self.cards) < (self.n_decks * 2):
            self.reset_table()
