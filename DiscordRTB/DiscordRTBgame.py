'''
Wojciech Gorzynski
04-06-2025 v1

an implementation of the "RideTheBus" game from a game called "Schedule 1"
tuned for use in a discord bot
'''
from DeckOfCards import Deck

class RideTheBus(Deck):
    def __init__(self, bet):
        super().__init__()
        self.shuffle()
        self.multiplier = 1
        self.cards_used = []
        self.bet = bet
        self.color_passed = False
        self.high_low_passed = False
        self.in_out_passed = False
        self.suit_passed = False
                 
    def color(self, choice):
        if self.last_card()[-1:] in ["D", "H"]:
            color = "Red"
        else:
            color = "Black"
        self.cards_used.append(self.last_card(1))

        if color == choice:
            self.multiplier = 2
            self.color_passed = True
            return True
        else:
            self.multiplier = 0
            return False
    
    def high_low(self, choice):
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
            self.high_low_passed = True
            self.multiplier = 3
            return True
        else:
            self.multiplier = 0
            return False
    
    def in_out(self, choice):
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
            self.in_out_passed = True
            self.multiplier = 4
            return True
        else:
            self.multiplier = 0
            return False
    
    def suit(self, choice):
        card = self.last_card(1)
        self.cards_used.append(card)
        
        if choice == card[-1:]:
            self.suit_passed = True
            self.multiplier = 20
            return True
        else:
            self.multiplier = 0
            return False
    
    def translate_value(self, card):
        card_value = card[:-1]
        values = {"J":11, "Q":12, "K":13, "A":14}
        for key, value in values.items():
            if card_value.count(key) == 1:
                return value
        return int(card_value)
    
    def string_card(self, card):
        card_suit = card[-1]
        suits = {"C":"Clubs", "D":"Diamonds", "H":"Hearts", "S":"Spades"}
        for key, value in suits.items():
            if card_suit.count(key) == 1:
                card_suit = value
        
        card_value = card[:-1]
        courts = {"J":"Jack", "Q":"Queen", "K":"King", "A":"Ace"}
        for key, value in courts.items():
            if card_value.count(key) == 1:
                card_value = value
        
        return card_value+" of "+card_suit   
        