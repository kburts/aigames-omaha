class Card(object):
    """
    Card class
    """
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.number = '23456789TJQKA'.find(value)

    def __str__(self):
        return self.value + self.suit

class Pocket(object):
    '''
    Pocket class
    '''
    def __init__(self, cards):
        self.cards = cards

    def __iter__(self):
            return iter(self.cards)

    def __str__(self):
        return str([str(card) for card in self.cards])

class Table(object):
    '''
    Table class
    '''
    def __init__(self, cards):
        self.cards = cards

    def __iter__(self):
            return iter(self.cards)
    def __str__(self):
        return str([str(card) for card in self.cards])

class Hand(object):
    '''
    Hand class
    '''
    def __init__(self, cards):
        self.cards = cards
        self.rank = Ranker.rank_five_cards(cards)

    def __gt__(self, hand):
        return self.rank > hand.rank

    def __ge__(self, hand):
        return self.rank >= hand.rank

    def __lt__(self, hand):
        return self.rank < hand.rank

    def __le__(self, hand):
        return self.rank <= hand.rank

    def __eq__(self, hand):
        return self.rank == hand.rank

class Ranker(object):
    '''
    Ranker class
    returns number + original cards.
    Number ranges from 0 - 16 with 0 being nothing and 16 being a royal flush
    '''
    @staticmethod
    def rank_five_cards(cards):

        # List of all card values
        values = sorted(['23456789TJQKA'.find(card.value) for card in cards])

        # Checks if hand is a straight
        is_straight = all([values[i] == values[0] + i for i in range(5)])

        # Additional straight check
        if not is_straight:

            # Weakest straight
            is_straight = all(values[i] == values[0] + i for i in range(4)) and values[4] == 12

            # Rotate values as the ace is weakest in this case
            values = values[1:] + values[:1]

        # Checks if hand is a flush
        is_flush = all([card.suit == cards[0].suit for card in cards])

        # Get card value counts
        value_count = {value: values.count(value) for value in values}

        # Sort value counts by most occuring
        sorted_value_count = sorted([(count, value) for value, count in value_count.items()], reverse = True)

        # Get all kinds (e.g. four of a kind, three of a kind, pair)
        kinds = [value_count[0] for value_count in sorted_value_count]

        # Get values for kinds
        kind_values = [value_count[1] for value_count in sorted_value_count]


        firstfour = all([values[i] == values[0] + i for i in range(4)])
        secondfour = all([values[i] == values[0] + i + 1 for i in range(4)])

        firstthree = all([values[i] == values[0] + i for i in range(3)])
        secondthree = all([values[i] == values[0] + i + 2 for i in range(3)])

        ## Hand strength
        strength = 0

        # Royal flush
        if is_straight and is_flush and values[0] == 8:
            strength = 16
        # Straight flush
        elif is_straight and is_flush:
            strength = 15
        # Four of a kind
        elif kinds[0] == 4:
            strength = 14
        # Full house
        elif kinds[0] == 3 and kinds[1] == 2:
            strength = 13
        # Flush
        elif is_flush:
            strength = 12
        # Straight
        elif is_straight:
            strength = 11
        ## Four to RF
        elif firstfour and all([card.suit == cards[0].suit for card in cards[:-1]]) or secondfour and all([card.suit == cards[0].suit for card in cards[1:]]):
            strength = 10
        # Three of a kind
        elif kinds[0] == 3:
            strength = 9
        # Two pair
        elif kinds[0] == 2 and kinds[1] == 2:
            strength = 8
        ## Single high pair
        elif kinds[0] == 2 and kind_values >= 9:
            strength = 7
        ## Four to a flush
        elif all([card.suit == cards[0].suit for card in cards[1:]]) or all([card.suit == cards[0].suit for card in cards[:-1]]):
            strength = 6
        ## Four to a straight
        elif all([values[i] == values[0] + i for i in range(4)]) or all([values[i] == values[0] + i + 1 for i in range(4)]):
            strength = 5
        ## Two to a RF
        elif firstthree and all([card.suit == cards[0].suit for card in cards[:-1]]) or secondthree and all([card.suit == cards[0].suit for card in cards[1:]]):
            strength = 4
        # Low Pair
        elif kinds[0] == 2:
            strength = 3
        ## Other crappy hands.
        else:
            strength = 0

        return [strength, [str(card) for card in cards]]

    @staticmethod
    def rank_single_hand(cards):
        from collections import Counter
        """
        Rank a 4 card starting hand and return it's power
        """
        suits = Counter([card.suit for card in cards])
        values = Counter([card.value for card in cards])

        suit_strength = 0
        value_strength = 0

        if len(suits) == 4:
            suit_strength = 1
        if len(suits) == 3:
            suit_strength = 2
        if len(suits) == 2:
            suit_strength = 4
            if suits.values()[0] == 2:
                ## Best possible hand, two sets of two suits
                suit_strength += 4
        if len(suits) == 1:
            suit_strength = 4

        for card, instances in values.iteritems():
            if card in 'JQKA':
                value_strength += 2 * instances
            if card in '89T':
                value_strength += 1 * instances
            if card in '234567':
                value_strength += 0.25 * instances

        return suit_strength * value_strength