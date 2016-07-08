import sys
from Card import *
class Hist(dict):
    ''' A map from each item(x) to its frequency '''
    def __init__(self, seq=[] ):
        "Creates a new histogram starting with the items in seq"
        for x in seq:
            self.count(x)
    def count(self, x, f=1):
        "Increments the counter associated with item x"
        self[x] = self.get(x,0) + f
        if self[x] == 0:
            del self[x]
class PokerHand(Hand):
    ''' Represents a poker hands'''
    all_labels = ['straightflush', 'fourkind', 'fullhouse', 'flush',
                  'straight', 'threekind','twopair','pair','highcard']
    def make_histograms(self):
        ''' Computes histograms for suits and hands
        Creates attributes:
        suits: a histogram of the suits in the hand
        ranks: a histogram of the ranks
        sets: a sorted list of the rank sets in the hand '''
        self.suits = Hist()
        self.ranks = Hist()
        for card in self.cards:
            self.suits.count(card.suit)
            self.ranks.count(card.rank)
        self.sets = self.ranks.values()
        self.sets.sort(reverse=True)

    def has_highcard(self):
        ''' Returns True if this hand has a high card '''
        return len(self.cards)
    def check_sets(self, *t):
        ''' Checks whether self.sets contains sets that are at least as big as 
        the requirements in t 
        t: list of int '''
        for need, have in zip(t, self.sets):
            if need > have: return False
        return True
    def has_pair(self):
        return self.check_sets(2)
    def has_twopair(self):
        return self.check_sets(2,2)
    def has_threekind(self):
        return self.check_sets(3)
    def has_fourkind(self):
        return self.check_sets(4)
    def has_fullhouse(self):
        return self.check_sets(3,2)
    def has_flush(self):
        ''' Returns True if the hand has a flush, Flase otherwise '''
        for val in self.suits.values():
            if val >= 5:
                return True
            return False
    def has_straight(self):
        # make a copy of the rank histogram before we mess with it
        ranks = self.ranks.copy()
        ranks[14] = ranks.get(1,0)
        # see if we have 5 in a row
        return self.in_a_row(ranks,5)
    def in_a_row(self,ranks,n):
        ''' checks whether the histogram has n ranks in a row 
        hist: map from rank to frequency
        n : number we need to get to '''
        count = 0
        for i in range(1,15):
            if ranks.get(i,0):
                count += 1
                if count == 5: return True
            else:
                count = 0
        return False
    def has_straightflush(self):
        # make a set of the (rank,suit) pairs 
        s = set()
        for card in self.cards:
            s.add( (card.rank, card.suit) )
            if card.rank == 1:
                s.add( (14, card.suit) )
        # iterate through the suits and ranks see if we get to 5 in a row
        for suit in range(4):
            count = 0
            for rank in range(1,15):
                if (rank, suit) in s:
                    count += 1
                    if count == 5 : return True
                else:
                    count = 0
        return False
    def has_straightflush2(self):
        # partition the hand by suit and check each sub-hand for a straight
        d = dict()
        for card in self.cards:
            d.setdefault( card.suit, PokerHand() ).add_card(card)
        # see if any of the partitioned hands has a straight
        for hand in d.values():
            if len(hand.card) < 5: continue
            hand.make_histograms()
            if hand.has_straight():
                return True
        return False
    def classify(self):
        self.make_histograms()
        self.labels = list()
        for label in PokerHand.all_labels:
            f = getattr(self, 'has_'+label)
            if f():
                self.labels.append(label)

class PorkerDeck(Deck):
    def deal_hands(deck, num_cards = 5, num_hands=10):
        hands = list()
        for i in range(num_hands):
            hand = PokerHand()
            deck.move_cards(hand, num_cards)
            hand.classify()
            hands.append(hand)
        return hands
def main(*args):
    # the label histogram : map from label to number of occurances
    lhist = Hist()
    # loop n times, dealing 7 hands per iteration, 7 cards each
    n= 10000
    for i in range(n):
        if i % 1000 == 0:
            print i
        deck = PorkerDeck()
        deck.shuffle()
        hands = deck.deal_hands(7,7)
        for hand in hands:
            for label in hand.labels:
                lhist.count(label)
    # print the results
    total = 7.0 * n
    print total, 'hands dealt:'
    for label in PokerHand.all_labels:
        freq = lhist.get(label,0)
        if freq == 0: continue
        p = total / freq
        print '%s happens one time in %.2f' %(label,p)

if __name__ =='__main__':
    main(*sys.argv)
