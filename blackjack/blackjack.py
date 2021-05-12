import random


las_vegas_table = { 8: {'2': 'H', '3': 'H', '4': 'H', '5': 'H', '6': 'H', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'J': 'H', 'Q': 'H', 'K': 'H', 'A': 'H'},
                    9: {'2': 'H', '3': 'D', '4': 'D', '5': 'D', '6': 'D', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'J': 'H', 'Q': 'H', 'K': 'H', 'A': 'H'},
                   10: {'2': 'D', '3': 'D', '4': 'D', '5': 'D', '6': 'D', '7': 'D', '8': 'D', '9': 'D', '10': 'H', 'J': 'H', 'Q': 'H', 'K': 'H', 'A': 'H'},
                   11: {'2': 'D', '3': 'D', '4': 'D', '5': 'D', '6': 'D', '7': 'D', '8': 'D', '9': 'D', '10': 'D', 'J': 'D', 'Q': 'D', 'K': 'D', 'A': 'H'},
                   12: {'2': 'H', '3': 'H', '4': 'S', '5': 'S', '6': 'S', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'J': 'H', 'Q': 'H', 'K': 'H', 'A': 'H'},
                   13: {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'J': 'H', 'Q': 'H', 'K': 'H', 'A': 'H'},
                   14: {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'J': 'H', 'Q': 'H', 'K': 'H', 'A': 'H'},
                   15: {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'J': 'H', 'Q': 'H', 'K': 'H', 'A': 'H'},
                   16: {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'J': 'H', 'Q': 'H', 'K': 'H', 'A': 'H'},
                   17: {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'S', '8': 'S', '9': 'S', '10': 'S', 'J': 'S', 'Q': 'S', 'K': 'S', 'A': 'S'}}


class BlackjackPlayer:
    table = None
    hands = None
    player = None
    dealer = False
    bet = 0

    def __init__(self, table, player, dealer=False):
        self.table = table
        self.player = player
        self.dealer = dealer
        self.reset_hands()

    def add_card(self, hand, card):
        self.hands[hand].append(card)

    def reset_hands(self):
        self.hands = [[], []]
        self.bet = 10

    def end(self, dealer_score):
        if dealer_score < self.score(0) < 22:
            self.player.win(self.bet)
        elif self.score(0) < dealer_score < 22:
            self.player.lose(self.bet)
        self.reset_hands()

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

    def play(self, dealer_up):
        if self.dealer:
            score = self.score(0)
            while score < 17:
                self.add_card(0, self.table.hit())
                score = self.score(0)
        else:
            move = self.play_las_vegas(dealer_up)
            while move != 'S':
                self.add_card(0, self.table.hit())
                if move == 'D':
                    self.bet *= 2
                    return
                move = self.play_las_vegas(dealer_up)

    def play_las_vegas(self, dealer_up):
        if self.score(0) < 8:
            return 'H'
        if self.score(0) > 17:
            return 'S'
        return las_vegas_table[self.score(0)][dealer_up]


class BlackjackTable:
    n_decks = 0
    cards = []
    players = []

    def __init__(self, n_decks=4):
        self.n_decks = n_decks
        self.reset_table()

    def reset_table(self):
        self.cards = []
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

    def play(self, verbose=False):
        self.players.append(BlackjackPlayer(self, None, dealer=True))
        self.deal()
        dealer_score = 0
        for p in self.players:
            p.play(self.players[-1].hands[0][0])
            if not p.dealer:
                if verbose:
                    print('Player ' + str(p.player.player_id) + ': ' + str(p.hands[0]) + '; score: ' + str(p.score(0)))
            else:
                dealer_score = p.score(0)
                if verbose:
                    print('Dealer: ' + str(p.hands[0]) + '; score: ' + str(p.score(0)))
        self.players.pop()
        for p in self.players:
            p.end(dealer_score)
        if len(self.cards) < (self.n_decks * 13 * 2):
            self.reset_table()
