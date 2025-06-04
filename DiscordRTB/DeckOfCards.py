'''
Wojciech Gorzynski
01-06-2025 v1

A program used for simulating a deck of cards
'''
from random import randint

class Deck:
    def __init__(self):
        self.cards = self.generate_deck()

    def generate_deck(self):
        deck = []
        for suit in "CDHS":
            for value in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]:
                deck.append(value+suit)
        return deck

    def reset(self):
        self.cards = self.generate_deck()
    
    def shuffle(self):
        temp = self.cards[:]
        newCards = []
        while len(temp) != 1:
            index = randint(0, len(temp)-1)
            newCards.append(temp[index])
            temp.pop(index)
        newCards.append(temp[0])
        self.cards = newCards    

    def random_card(self, removeFlag = False):
        if removeFlag:
            index = randint(0, len(self.cards)-1)
            card = self.cards[index]
            self.cards.pop(index)
            return card            
        else:
            return self.cards[randint(0, len(self.cards)-1)]
        
    def last_card(self, removeFlag = False):
        if removeFlag:
            index = len(self.cards)-1
            card = self.cards[index]
            self.cards.pop(index)
            return card
        else:
            return self.cards[len(self.cards)-1]