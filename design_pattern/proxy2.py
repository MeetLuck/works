# you - DebitCard(proxy) - Bank

class You(object):
    def __init__(self):
        print "You -> Let's buy the Denim shirt"
        self.debitCard = DebitCard()
        self.isPurchased = False
    def make_payment(self):
        self.isPurchased = self.debitCard.do_pay()
    def __del__(self):
        if self.isPurchased:
            print 'You -> Wow! Denim shirt is Mine :-)'
        else:
            print 'You -> I should earn more :('

from abc import ABCMeta, abstractmethod
class Payment(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def do_pay(self):
        pass
class Bank(Payment):
    def __init__(self):
        self.card = None
        self.account = None
    def getAccount(self):
        self.account = self.card # card number is account number
        return self.account
    def hasFunds(self):
        print 'Bank -> Checking if Account', self.getAccount(),'has enough founds'
        return True
    def setCard(self,card):
        self.card = card
    def do_pay(self):
        if self.hasFunds():
            print 'Bank -> Paying the merchant'
            return True
        else:
            print 'Bank -> Sorry, not enough funds!'
            return False

class DebitCard(Payment):
    def __init__(self):
        self.bank = Bank()
    def do_pay(self):
        card = input('DebitCard -> Enter Card Number: ')
        self.bank.setCard(card)
        return self.bank.do_pay()


if __name__ == '__main__':
    you = You()
#   debitcard = DebitCard()
    you.make_payment()
