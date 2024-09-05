import random
import os

class DiceFace():
    def __init__(self, damage = 0, block = 0):
        self.block = block
        self.damage = damage
    def ExecuteDice(self, target, user):
        target.TakeDamage(self.damage)
        user.block += self.block

    
class Dice():
    def __init__(self):
        self.faces = [DiceFace(i) for i in range(1,7)]
    def Roll(self):
        return self.faces[random.randint(0,5)]

class Enemy():
    def __init__(self, maxhealth = 25, name = "slime", damage = 5):
        self.maxHealth = maxhealth
        self.health = maxhealth
        self.damage = damage
        self.name = name
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
        self.alive = True
        self.score = 0
        self.block = 0
        self.coins = 500
    
    def TakeDamage(self, damage):
        # Apply block to damage first
        if self.block > 0:
            if damage >= self.block:
                damage -= self.block
                self.block = 0  # Block is used up
            else:
                self.block -= damage
                damage = 0  # All damage was absorbed by the block

        # Apply remaining damage to health
        if damage > 0:
            self.health -= damage

            if self.health > self.maxHealth:
                self.health = self.maxHealth
        self.DeathCheck()
    
    def Turn(self, enemy):
        if self.health >= 0 :
            pass
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
                    diceResults[diceIndex].ExecuteDice(enemy, self)
                    diceResults.pop(diceIndex)
                else:
                    print("That dice doesn't exist.")
            except ValueError:
                print("Enter the NUMBER of the dice or 'x' to end the turn.")
            except IndexError:
                print("Invalid input. Please enter a valid dice number or 'x' to end the turn.")
   
    def DisplayStats(self):
        print(f"Health : {self.health}/{self.maxHealth}\nBlock : {self.block}\n")

    def ShowDiceValues(self):
        for dice in range(len(self.Dice)):
            print(f"Dice {dice} : ")
            for diceFace in range(len(self.Dice[dice].faces)):
                print(f"    Face: {diceFace}  damage :{self.Dice[dice].faces[diceFace].damage}, block : {self.Dice[dice].faces[diceFace].block}")
    
    def UpgradeDice(self, upgrades):
        upgradePoints = upgrades
        print(f"Pick a dice dice to upgrade (Upgrade Points: {upgradePoints})")
        errorBool = False
        error = None
        while upgradePoints > 0:
            while True:
                os.system("cls")
                if errorBool == True:
                    print("Please enter a valid number ")
                self.ShowDiceValues()
                print(f"You have {upgradePoints} upgrades left! ")
                diceIndex = input("Enter a dice index ")
                faceIndex =  input("Enter a dice face index ")
                try:
                    diceIndex = int(diceIndex)
                    faceIndex = int(faceIndex)
                    self.Dice[diceIndex].faces[faceIndex].block += 1
                    self.Dice[diceIndex].faces[faceIndex].damage += 1
                    errorBool = False
                    upgradePoints -= 1
                    break
                except ValueError:
                    errorBool = True
                except IndexError:
                    errorBool = True

    def DeathCheck(self):
        if self.health <= 0:
            self.alive = False

    def Heal(self, heal_amount):
        self.health += heal_amount
        if self.health > self.maxHealth:
            self.health = self.maxHealth

class Map():
    def __init__(self):
        self.location = 0
        self.previous_location = 5
        '''
        0 will be enemy
        1 will be pool
        2 will be altar
        3 will be shop
        4 will be boss
        '''
    def NewRoom(self):
        self.previous_location = self.location
        while self.previous_location == self.location:
            self.location = random.randint(0,3)
        player.score += 1

        if self.location == 0:
            self.EnemyRoom()
        elif self.location == 1:
            self.Pool()
        elif self.location == 2:
            self.Altar()
        elif self.location == 3:
            self.Shop()
            
    def EnemyRoom(self, EnemyGiven=0):
        if EnemyGiven == 0:
            enemy = Enemy()
        else:
            enemy = EnemyGiven

        enemy_coins= enemy.maxHealth

        print(f"{enemy.health > 0  and player.alive}")

        while enemy.health > 0 and player.alive:
            player.Turn(enemy)
            enemy.EnemyTurn(player)
            
        if enemy.health < 0:
            input(f"You killed the {enemy.name}! ")
            player.coins += enemy_coins

    def Pool(self):
        while True:
            os.system("cls")
            choice = input("You see a pool ahead\nDo you dive in?\n1.) Yes\n2.) No\n")
            try:
                choice = int(choice)
                if choice < 0 < 2:
                    raise ValueError
                break
            except ValueError:
                print("Select a valid option")
        if choice == 1:
            reward = random.randint(1,2)
            if reward == 2:
                print("You found an upgrade!\n")
                input()
                player.UpgradeDice(random.randint(1,2))
                
            else:
                print("It was a trap!\nYou took 10 damage!")
                player.TakeDamage(10)
                input()

        elif choice == 1:
            print("You leave the pool alone...")
            input()

    def Altar(self):
        choice = ""
        while True:
            os.system("cls")
            choice = input("You see an omnious altar ahead...\nDo you place your hand upon it?\n1.)Yes \n2.)No\n ")
            try:
                choice = int(choice)
                if choice == 1 or choice == 2:
                    break
                else:
                    break
                
            except ValueError:
                print("please enter a valid number")
        if choice == 1:
            result = random.randint(0,2)
            if result == 0:
                print("You found a new dice! ")
                player.Dice.append(Dice())
            if result == 1:
                print("You found multiple upgrades! ")
                player.UpgradeDice(5)
            if result == 2:
                input("You hear something rumbling from below... ")
                map.EnemyRoom(EnemyGiven=Enemy(maxhealth=100, name="curiosity", damage = 10))

        else:
            print("You left the altar alone...\nMaybe the better choice\n")
        input()

    def Shop(self):
        x = ""

        while x != "x":
            os.system("cls")
            x = input(f"You fouond a shop... \nYou have {player.coins} coins\n1.) Health potion (+20 HP) (25 coins)\n2.) Max Heal (75 coins)\n3.) Dice Upgrade (100 coins)\n4.) New Dice (200 coins) \nx.) leave shop \n")
            if x == "1" and player.coins > 25:
                player.coins -= 25
            elif x == "2" and player.coins > 75:
                player.coins -= 75
                player.health = player.maxHealth
            elif x == "3" and player.coins > 100:
                player.coins -= 100
                player.UpgradeDice(1)
            elif x == "4" and player.coins > 200:
                player.coins -= 200
                player.Dice.append(Dice())
                




###################################################
map = Map()
player = Player(dice = [Dice()])

while player.health > 0:
    map.NewRoom()
if player.alive == False:
    print(f"You have died!\nYour score was {player.score}")
