

class Wallet:
    def __init__(self, id):
        self.balance = 0
        self.id = id
        with open("RTB_balance.txt", "w+t") as file:
            file.write(f"{self.id}  {self.balance}\n")    
    
    def get_balance(self):
        with open("RTB_balance.txt", "r+t") as file:
            return [int(account.replace("\n","").split()[1]) for account in file.readlines() if account.replace("\n","").split()[0] == self.id][0]

    def change_balance(self, n):
        with open("RTB_balance.txt", "r+t") as file:
            print(file.readlines())
            accounts = file.readlines()[file.readlines().index(f"{self.id}  {self.get_balance()}\n")] = f"{self.id}  {self.get_balance()+n}\n" 
        with open("RTB_balance.txt", "w+t") as file:
            file.write(accounts)
        
wallet = Wallet("first")
print(wallet.change_balance(100))
