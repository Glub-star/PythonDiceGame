import random
import os

class DiceFace():
    def __init__(self, damage = 0, block = 0):
        self.block = block
        self.damage = damage
    def ExecuteDice(self, target):
        target.TakeDamage(self.damage)
    
class Dice():
    def __init__(self):
        self.faces = [DiceFace(i) for i in range(1,7)]
    def Roll(self):
        return self.faces[random.randint(0,5)]

class Enemy():
    def __init__(self):
        self.health = 50
        self.maxHealth = 50
        self.damage = 10
        self.name = "slime"
    def TakeDamage(self, damage):
        self.health -= damage
    def EnemyTurn(self, target):
        target.TakeDamage(self.damage)
    def DisplayStats(self):
        print(f"{self.name} : \n Health : {self.health}/{self.maxHealth}\n Damage: {self.damage}\n")

class Player():
    def __init__(self,dice):
        self.health = 100
        self.maxHealth = 100
        self.Dice = [*dice]
    
    def TakeDamage(self, damage):
        self.health -= damage
    
    def Turn(self, enemy):
        # Display the dice results
        diceResults = [dice.Roll() for dice in self.Dice]
        while True:
            os.system("cls")  # Clear the screen (use "clear" on Unix systems)
            self.DisplayStats()
            enemy.DisplayStats()
            for i, dice in enumerate(diceResults):
                print(f"{i}.) Damage: {dice.damage}, Block: {dice.block}")
            print("x.) End turn")

            try:
                choice = input("What dice do you want to play? ").strip()
                if choice == "x":
                    break
                diceIndex = int(choice)
                if 0 <= diceIndex < len(diceResults):
                    diceResults[diceIndex].ExecuteDice(enemy)
                    diceResults.pop(diceIndex)
                else:
                    print("That dice doesn't exist.")
            except ValueError:
                print("Enter the NUMBER of the dice or 'x' to end the turn.")
            except IndexError:
                print("Invalid input. Please enter a valid dice number or 'x' to end the turn.")
    def DisplayStats(self):
        print(f"Health : {self.health}/{self.maxHealth}\n")

    def ShowDiceValues(self):
        for dice in range(len(self.Dice)):
            print(f"Dice {dice} : ")
            for diceFace in range(len(self.Dice[dice].faces)):
                print(f"    Face: {diceFace}  damage :{self.Dice[dice].faces[diceFace].damage}, block : {self.Dice[dice].faces[diceFace].block}")
    
    def UpgradeDice(self, upgrades):
        upgradePoints = upgrades
        print(f"Pick a dice dice to upgrade (Upgrade Points: {upgradePoints})")
        self.ShowDiceValues()
        while upgradePoints > 0:
            while True:
                diceIndex = input("Enter a dice index ")
                faceIndex =  input("Enter a dice face index ")
                try:
                    diceIndex = int(diceIndex)
                    faceIndex = int(faceIndex)
                except ValueError:
                    print("Please enter a number")
                    
                
                

class Map():
    def __init__(self):
        self.location = 0
        '''
        0 will be enemy
        1 will be pool
        2 will be altar
        3 will be shop
        4 will be boss
        '''
    def NewRoom(self):
        self.location = random.randint(0,3)
        
def EnemyRoom():
    enemy = Enemy()
    while enemy.health > 0:
        enemy.EnemyTurn()
        player.Turn()

def Pool():
    while True:
        os.system("cls")
        choice = input("You see a pool ahead\nDo you dive in?\n1.) Yes\n2.) No")
        try:
            choice = int(choice)
            if choice < 0 < 2:
                raise ValueError
            break
        except ValueError:
            print("Selecta a valid option")
    if choice == 0:
        reward = random.randint(1,2)
        if reward == 1:
            print("You found an upgrade!\n")
            ###############################
        else:
            print("It was a trap!\nYou took 10 damage!")
            player.health -= 10

    elif choice == 1:
        print("You leave the pool alone...")


player = Player(dice = [Dice(),Dice(),Dice()])

player.ShowDiceValues()
