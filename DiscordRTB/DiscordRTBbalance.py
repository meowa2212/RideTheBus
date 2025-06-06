'''
Wojciech Gorzynski
06-06-2025 v1
A class used for control over player balances for a Discord bot
'''
import os

class Wallet:
    def __init__(self, id, file_name):
        self.file_name = file_name
        
        if not os.path.exists(self.file_name):
            open(self.file_name, "w").close()
            
        self.id = str(id)
        if not self.on_list():
            with open(self.file_name, "a+t") as file:
                file.write(f"{self.id}\t{0}\n")    
    
    def on_list(self):
        with open(self.file_name, "r+t") as file:
            accounts = [tuple(x.replace("\n", "").split()) for x in file.readlines()]
        for account in accounts:
            if self.id == account[0]:
                return True
        return False
    
    def get_balance(self):
        with open(self.file_name, "r+t") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2 and parts[0] == self.id:
                    return int(parts[1])
    
    def set_balance(self, amount):
        with open(self.file_name, "r+t") as file:
            accounts = [tuple(x.replace("\n", "").split()) for x in file.readlines()]
        accounts = [x[0]+"\t"+str(amount)+"\n" if x[0] == self.id else x[0]+"\t"+x[1]+"\n" for x in accounts]
        
        with open(self.file_name, "w+t") as file:
            for account in accounts:
                file.write(account)
    
    def ranking(self):
        with open(self.file_name, "r+t") as file:
            accounts = [tuple(x.replace("\n", "").split()) for x in file.readlines()]
        accounts.sort(key = lambda x: x[1], reverse = True)
        return accounts
        
    
    def change_balance(self, amount):
        self.set_balance(self.get_balance()+amount)
        
