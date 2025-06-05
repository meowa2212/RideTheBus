'''
Wojciech Gorzynski
04-06-2025 v1

an implementation of the "RideTheBus" game from a game called "Schedule 1"
tuned for use in a discord bot
'''
from DeckOfCards import Deck

class RideTheBus(Deck):
    def __init__(self, balance, bet):
        print("starting game")
        super().__init__()
        self.shuffle()
        self.balance = balance - bet
        self.multiplier = 1
        self.cards_used = []
        self.bet = bet
        self.color_passed = False
        self.high_low_passed = False
        self.in_out_passed = False
        self.suit_passed = False
                 
    def color(self, choice):
        print("starting color")
        print(self.last_card())
        if self.last_card()[-1:] in ["D", "H"]:
            color = "Red"
        else:
            color = "Black"
        self.cards_used.append(self.last_card(1))

        if color == choice:
            self.multiplier = 2
            print("color won")
            return True
        else:
            self.multiplier = 0
            print("color lost")
            return False
    
    def high_low(self, choice):
        print("starting high_low")
        print(self.last_card())
        value_last = self.translate_value(self.cards_used[0])
        while True:
            card = self.last_card(1)
            value = self.translate_value(card)
            if value != value_last:
                break

        if value > value_last:
            height = "High"
            self.cards_used.append(card)
        else:
            height = "Low"
            self.cards_used.insert(0, card)
        
        if height == choice:
            self.multiplier = 3
            print("high_low won")
            return True
        else:
            self.multiplier = 0
            print("high_low lost")
            return False
    
    def in_out(self, choice):
        print("starting in_out")
        print(self.last_card())
        value_start = self.translate_value(self.cards_used[0])
        value_end = self.translate_value(self.cards_used[1])
        while True:
            card = self.last_card(1)
            value = self.translate_value(card)
            if value not in [value_start, value_end]:
                break
        self.cards_used.append(card)
    
        if value_start < value < value_end:
            stand = "In"
        else:
            stand = "Out"    
        
        if choice == stand:
            self.multiplier = 4
            print("in_out won")
            return True
        else:
            self.multiplier = 0
            print("in_out lost")
            return False
    
    def suit(self, choice):
        print("starting suit")
        print(self.last_card())
        card = self.last_card(1)
        self.cards_used.append(card)
        
        if choice.capitalize()[0] == card[-1:]:
            print("suit won")
            return True
        else:
            self.multiplier = 0
            print("suit lost")
            return False
    
    def translate_value(self, card):
        card_value = card[:-1]
        values = {"J":11, "Q":12, "K":13, "A":14}
        return values.get(card_value, int(card_value))
