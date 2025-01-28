import numpy as np
from cards import read_card, hand_score
from tree import DecisionTree, Features
from enum import Enum
'''
    Values for Matrix           max_amount = amount_of_players * starting_balance 
    HAND_SCORE = 0              ( 0 - 9 )
    HIGH_CARD_SCORE = 1 -       ( 0 - 12 )
    BET = 2                     ( 0 - max_amount )
    BALANCE = 3                 ( 0 - max_amount )
    AMOUNT_PLACED = 4           ( 0 - max_amount )
    ROUND = 5                   ( 1- 10 )
'''

class Player_actions(Enum):
    FOLD = 0
    CHECK = 1
    RISE = 2

class Player:
    def __init__(self, index, amount_of_players, starting_balance, max_depth=5):
        self.index = index
        self.name = f'Player {self.index}'
        self.wins = 0
        self.starting_balance = starting_balance
        self.balance = starting_balance
        self.amount_placed = 0
        self.score = 0
        self.cards = []
        self.high_card = 0
        max_amount = amount_of_players * starting_balance
        self.tree = DecisionTree(
            max_depth=max_depth, 
            M_treshholds = np.array(    # Restricts how tresholds are choosen
                [[0, 0, 0, 0, 0, 1],
                [9, 12, max_amount, max_amount, max_amount, 10]]))
        x = np.zeros(len(Features))
        label= np.arange( len(Player_actions) )
        self.tree.create(x,label)

    def __str__(self):
        output = f'Player {self.index}\n'
        output += f'Wins: {self.wins}\n'
        output += f'Balance: {self.balance}\n'

        return output

    def reset_player(self):
        self.wins = 0
        self.balance = self.starting_balance

    def add_cards(self, cards):
        # Addin cards means start of the new game
        self.amount_placed = 0
        self.score = 0
        self.high_card = 0
        self.cards = cards
        self.find_high_card()

    def display_hand(self, community_cards):
        print(f"{self.name}'s hand")
        for card in self.cards:
            print(read_card(card))

        for card in community_cards:
            print(read_card(card))

    def calculate_score(self, community_cards):
        self.score = hand_score(self.cards, community_cards)
        return self.score

    def find_high_card(self):
        scores = []
        for card in self.cards:
            scores.append(card[0])

        self.high_card = np.max(np.array(scores))
    
    def make_decision(self, bet, rise_amount, n_round):
        features = np.zeros(len(Features))
        features[Features.HAND_SCORE.value] = self.score
        features[Features.HIGH_CARD_SCORE.value] = self.high_card
        features[Features.BET.value] = bet
        features[Features.BALANCE.value] = self.balance
        features[Features.AMOUNT_PLACED.value] = self.amount_placed
        features[Features.ROUND.value] = n_round

        out = self.tree.predict(features)
        if out == Player_actions.RISE.value:
            # Doesn't let player bet more than he has
            if (bet+rise_amount)>self.balance:
                out = Player_actions.CHECK.value
            else:
                out = Player_actions.RISE.value

        return out

    def add_bet(self, bet):
        change = bet - self.amount_placed
        if change > self.balance:
            return -1
        self.balance -= change
        self.amount_placed += change
        return change

    def add_win(self, amount):
        self.balance += amount
        self.wins += 1

    def get_score(self):
        return self.score

    def get_high_card(self):
        self.find_high_card()
        return self.high_card

    def visualise_strategy(self):
        name = f'{self.name}s strategy'
        self.tree.visualize_tree(name)
