'''
Wojciech Gorzynski
01-06-2025 v1

an implementation of the "RideTheBus" game from a game called "Schedule 1"
'''
from DeckOfCards import Deck

class RideTheBus(Deck):
    def __init__(self, balance):
        super().__init__()
        self.balance = balance
        self.multiplier = 1
        self.cards_used = []

    def play_game(self):
        self.shuffle()
        print("Welcome!")
        print(f"Balance: {self.balance}$")
        self.bet = int(input("Place your bet: "))
        self.clear_scene()
        self.balance -= self.bet

        if self.color(input("Red or Black: ")):
            self.clear_scene()
            print(self.cards_used)
            if self.high_low(input("High or Low: ")):
                self.clear_scene()
                print(self.cards_used)
                if self.in_out(input("In or Out: ")):
                    self.clear_scene()
                    print(self.cards_used)
                    if self.suit(input("Clubs, Diamonds, Hearts or Spades: ")):
                        print(self.cards_used)
        self.end_game()
                 
    def color(self, choice):
        self.clear_scene()
        
        if self.last_card()[-1:] in ["D", "H"]:
            color = "Red"
        else:
            color = "Black"
        self.cards_used.append(self.last_card())
        print(f"Card: {self.last_card(1)}")
        print(f"Color: {color}")
        if color == choice:
            self.multiplier = 2
            if self.next_stage():
                return True
            else:
                return False
        else:
            self.multiplier = 0
            return False
    
    def high_low(self, choice):
        self.clear_scene()
        
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
        print(f"Card: {card}")
        print(f"Height: {height}")
        
        if height == choice:
            self.multiplier = 3
            if self.next_stage():
                return True
            else:
                return False
        else:
            self.multiplier = 0
            return False
    
    def in_out(self, choice):
        self.clear_scene()
        
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
        print(f"Card: {card}")
        print(f"Stand: {stand}")
        
        if choice == stand:
            self.multiplier = 4
            if self.next_stage():
                return True
            else:
                return False
        else:
            self.multiplier = 0
            return False
    
    def suit(self, choice):
        self.clear_scene()
        
        card = self.last_card(1)
        self.cards_used.append(card)
        print(f"Card: {card}")
        print(f"Suit: {card[-1:]}")
        
        if choice.capitalize()[0] == card[-1:]:
            self.multiplier = 20
            return True
        else:
            self.multiplier = 0
            return False
    
    def translate_value(self, card):
        card_value = card[:-1]
        values = {"J":11, "Q":12, "K":13, "A":14}
        return values.get(card_value, int(card_value))
    
    def choice(self, message):
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
    
    def next_stage(self):
        print("Next Stage")
        print(f"Payout: {self.bet*self.multiplier}$")
        if self.choice("Continue?"):
            return True
        else:
            return False
    
    def end_game(self):
        print("End of game!")
        print(f"Payout: {self.bet*self.multiplier}$")
        self.balance += self.bet*self.multiplier
        print(f"Balance: {self.balance}$")
    
    def clear_scene(self):
        print("=====RideTheBus====Meowa====")     
            

if __name__ == "__main__":
    game = RideTheBus(0)
    game.play_game()