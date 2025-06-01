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

    def play_game(self):
        super().reset()
        self.shuffle()
        print("Welcome!")
        print(f"Balance: {self.balance}$")
        self.bet = int(input("Place your bet: "))
        self.balance -= self.bet
        self.color(input("Red or Black: "))

    def color(self, choice):
        color = ""
        if self.last_card()[-1:] in ["D", "H"]:
            color = "Red"
        else:
            color = "Black"
        print(f"Card: {self.last_card(1)}")
        print(f"Color: {color}")
        if color == choice:
            self.bet *= 2
            self.end_game()
        else:
            self.bet = 0
            self.end_game()
    
    def end_game(self):
        print("End of game!")
        print(f"Payout: {self.bet}$")
        self.balance += self.bet
        print(f"Balance: {self.balance}$")
        
        while True:
            choice = input("Play Again (Y/n): ").capitalize()[0]
            if choice in ["Y", "N"]:
                break
            else:
                print("Wrong Choice")

        if choice == "Y":
            print("Next Game")
            self.play_game()
        elif choice == "N":
            print("Thanks For Playing!")
        
            

if __name__ == "__main__":
    game = RideTheBus(500)
    game.play_game()