''' Card.py '''
import random
class Card(object):
    ''' Represents a standard playing card.
    Attributes:  suit: 0,1,2,3
                 rank: 1,2,...,13
    '''
    suit_names = ['Clubs','Diamonds','Hearts','Spades']
    rank_names = [ None, 'Ace', '2','3','4','5','6','7','8','9','10',
                    'Jack', 'Queen', 'King' ]
    def __init__(self, suit = 0, rank = 2):
        self.suit, self.rank = suit, rank
    def __str__(self):
        return '%s(%s)' %( Card.rank_names[self.rank], Card.suit_names[self.suit] )
    def __cmp__(self, other):
        card1 = self.suit, self.rank
        card2 = other.suit, other.rank
        return cmp(card1, card2)
class Deck(object):
    ''' Represents a deck of cards
    Attributes:  cards: [ list of Card objects ] '''
    def __init__(self):
        self.cards = list()
        for suit in range(4):
            for rank in range(1,14):
                card = Card(suit, rank)
                self.cards.append(card)
    def __str__(self):
        res = list()
        for card in self.cards:
            res.append( str(card) )
        return str(res)
#       return '\n'.join(res)
    def add_card(self, card):
        ''' Adds a card to the deck '''
        self.cards.append(card)
    def remove_card(self, card):
        ''' Removes a card from the deck '''
        self.cards.remove(card)
    def pop_card(self, i = -1):
        ''' Removes and returns a card from the deck
        i : index of the card to pop, by default, pops the last card 
        '''
        return self.cards.pop(i)
    def shuffle(self):
        ''' Suffles the cards in the deck '''
        random.shuffle(self.cards)
    def sort(self):
        ''' Sort the cards in ascending order '''
        self.cards.sort()
    def move_cards(self, hand, num):
        ''' Moves the given number of cards from the deck into Hand
        hand : destination Hand object
        num  : number of cards to move '''
        for i in range(num):
            hand.add_card( self.pop_card() )
class Hand(Deck):
    ''' Represents a hand of playing cards '''
    def __init__(self,label =''):
        self.cards = list()
        self.label = label
def find_defining_class(obj, method_name):
    for ty in type(obj).mro():
        if method_name in ty.__dict__:
            return ty
    return None

if __name__ == '__main__':
    deck = Deck()
    deck.shuffle()
    hand = Hand()
    print find_defining_class(hand, 'shuffle')
    deck.move_cards(hand, 5)
    hand.sort()
    print hand


