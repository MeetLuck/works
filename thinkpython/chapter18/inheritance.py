''' Chapter 18 Inheritance '''
import random
#------------- 18.1 Card objects ---------------------------
class Card(object):
    ''' Represents a standard playing card '''
    suit_names = ['Clubs', 'Diamonds', 'Hearts','Spades']
    rank_names = [None,'Ace','2','3','4','5','6','7','8','9','10',
                    'Jack', 'Queen','King']
    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return '%s of %s' %(Card.rank_names[self.rank], Card.suit_names[self.suit] )
    def __cmp__(self,other):
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return comp(t1,t2)
#------------- 18.2 Class attributes ---------------------------
card1 = Card(2,11)
print card1
#------------- 18.3 Comparing cards ---------------------------
# built-in cmp has the same interface as the method __cmp__:
# it takes two values and returns a positive number if the first is larger, a negative number
# if the second is larger, and 0 if they are equal
#------------- 18.4 Decks ---------------------------------------
class Deck(object):
    def __init__(self):
        self.cards = []
        for suit in range(4): # 0,1,2,3
            for rank in range(1,14): # 1,2,3,...,13
                card = Card(suit, rank)
                self.cards.append(card)
    def __str__(self):
        res = []
        for card in self.cards:
            res.append( str(card) )
        return '\n'.join(res)
    def pop_card(self):
        return self.cards.pop()
    def add_card(self,card):
        self.cards.append(card)
    def shuffle(self):
        random.shuffle(self.cards)
    def move_cards(self, hand, num):
        for i in range(num):
            hand.add_card( self.pop_card() )
    def deal_hands(self, num_of_hands, cards_per_hand):
        hands = []
        for h in range(num_of_hands):
            hand = Hand(str(h))
            self.move_cards(hand,7)
            hands.append(hand)
        return hands


#------------- 18.5 Printing the deck  ---------------------------
deck = Deck()
print deck
#------------- 18.6  Add, remove, shuffle and sort  --------------

#------------- 18.7  Inheritance ---------------------------------
class Hand(Deck):
    ''' Represents a hand of playing cards. '''
    def __init__(self, label=''):
        self.cards = []
        self.label = label
hand = Hand('new hand')
deck = Deck()
card = deck.pop_card()
hand.add_card(card)
print hand
#------------- 18.7  Inheritance ---------------------------------

#------------- 18.8  Debugging ---------------------------------
# use the 'mro' method to get the list of class object(types) that
# will be searched for method. Method Resolution Order
def find_defining_class(obj, method):
    for ty in type(obj).mro():
        if method in ty.__dict__:
            return ty
print find_defining_class(hand, 'shuffle')
