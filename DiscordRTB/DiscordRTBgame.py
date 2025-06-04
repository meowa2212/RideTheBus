'''
Wojciech Gorzynski
04-06-2025 v1

an implementation of the "RideTheBus" game from a game called "Schedule 1"
tuned for use in a discord bot
'''
from DeckOfCards import Deck

class RideTheBus(Deck):
    def __init__(self, balance, bet):
        super().__init__()
        self.shuffle()
        self.balance = balance - bet
        self.multiplier = 1
        self.cards_used = []
        self.bet = bet

    def play_game(self):
        self.shuffle()
        self.bet = int(input("Place your bet: "))
        
        self.balance -= self.bet

        if self.color(input("Red or Black: ")):
            
            print(self.cards_used)
            if self.high_low(input("High or Low: ")):
                
                print(self.cards_used)
                if self.in_out(input("In or Out: ")):
                    
                    print(self.cards_used)
                    if self.suit(input("Clubs, Diamonds, Hearts or Spades: ")):
                        print(self.cards_used)
        self.end_game()
                 
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
            self.multiplier = 4
            return True
        else:
            self.multiplier = 0
            return False
    
    def suit(self, choice):
        card = self.last_card(1)
        self.cards_used.append(card)
        
        if choice.capitalize()[0] == card[-1:]:
            return True
        else:
            self.multiplier = 0
            return False
    
    def translate_value(self, card):
        card_value = card[:-1]
        values = {"J":11, "Q":12, "K":13, "A":14}
        return values.get(card_value, int(card_value))
    
    def choice(self, message): #needs to be rewritten
        while True:
            choice = input(f"{message} (y/n): ").capitalize()[0]
            if choice in ["Y", "N"]:
                break
            else:
                print("Wrong Choice")

        if choice == "Y":
            return True
        elif choice == "N":
            return False
    
    def next_stage(self): #needs to be rewritten
        print("Next Stage")
        print(f"Payout: {self.bet*self.multiplier}$")
        if self.choice("Continue?"):
            return True
        else:
            return False
    
    def end_game(self):
        self.balance += self.bet*self.multiplier