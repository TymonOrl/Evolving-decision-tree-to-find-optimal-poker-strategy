from enum import Enum
from collections import Counter
import random
import numpy as np


class Suits(Enum):
    HEARTS = 0
    DIAMONDS = 1
    CLUBS = 2
    SPADES = 3

class Ranks(Enum):
    TWO = 0
    THREE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    EIGHT = 6
    NINE = 7
    TEN = 8
    JACK = 9
    QUEEN = 10
    KING = 11
    ACE = 12

class Hand_ranking(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9

class Deck:
    def __init__(self):
        self.cards = self.new_deck()
        self.shuffle_deck()

    def new_deck(self):
        cards = [(rank.value, suit.value) for rank in Ranks for suit in Suits]
        return cards

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def deal_cards(self):
        return [self.cards.pop(), self.cards.pop()]
    
    def first_draw(self):
        return [self.cards.pop(), self.cards.pop(), self.cards.pop()]
    
    def next_draw(self):
        return [self.cards.pop()]
    

def read_card(card_numbers: tuple) -> str:
    return Ranks(card_numbers[0]).name + ' ' + Suits(card_numbers[1]).name

def hand_score(hand, community_cards):
    '''
        Function returns score of joined cards of hand and community_cards
    '''
    all_cards = hand + community_cards
    ranks = sorted([card[0] for card in all_cards])

    is_flush = len(set(card[1] for card in all_cards)) == 1

    is_straight = ranks == list(range(ranks[0], ranks[0] + len(ranks)))

    rank_count = Counter(card[0] for card in all_cards)
    most_common = rank_count.most_common()
    
    if is_flush and is_straight and ranks[-1] == Ranks.ACE.value:
        return Hand_ranking.ROYAL_FLUSH.value
    if is_flush and is_straight:
        return Hand_ranking.STRAIGHT_FLUSH.value
    if most_common[0][1] == 4:
        return Hand_ranking.FOUR_OF_A_KIND.value
    if most_common[0][1] == 3 and most_common[1][1] == 2:
        return Hand_ranking.FULL_HOUSE.value
    if is_flush:
        return Hand_ranking.FLUSH.value
    if is_straight:
        return Hand_ranking.STRAIGHT.value
    if most_common[0][1] == 3:
        return Hand_ranking.THREE_OF_A_KIND.value
    if most_common[0][1] == 2 and len(most_common) == 3:
        return Hand_ranking.TWO_PAIR.value
    if most_common[0][1] == 2:
        return Hand_ranking.ONE_PAIR.value
    return Hand_ranking.HIGH_CARD.value
