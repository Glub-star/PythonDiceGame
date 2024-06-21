import random
import os

tutorial = True

def CC():
    os.system('cls' if os.name == 'nt' else 'clear')

class Dice():
    def __init__(self):
        self.sides = []

    def AddSide(self,sideToAdd):
        self.sides.append(sideToAdd)
    
    def Roll(self):
        return random.randint(0,len(self.sides))


class Player():
    def __init__(self):
        
        self.dice = Dice()

while True:
    print(random.randint(0,5))