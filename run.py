#Imports

from pyfiglet import Figlet
#import colorama
import os
import termios
import sys
import tty
import math
import random


#Variable declarations

f = Figlet(font="slant")
screenX = 80
screenY = 24
inkey_buffer = 1
current_level = 1
running = False
enemies = []

#Ascii art

boxFullAscii = [
    "+---+",
    "| i |",
    "+---+"
]

boxEmptyAscii = [
    "+---+",
    "|   |",
    "+---+"
]

doorClosedAscii = [
    "+--+",
    "||||",
    "||||",
    "+--+"
]

doorOpenAscii = [
    "+--+",
    "|  |",
    "|  |",
    "+--+"
]


#Class definitions


class Enemy:
    """
    Generic class for enemies, defining their variables and functions
    """
    def __init__(self, baseHealth, attack, hitChance, xPos, yPos, char):
        self.baseHealth = baseHealth
        self.health = baseHealth
        self.attack = attack
        self.hitChance = hitChance
        self.xPos = xPos
        self.yPos = yPos
        self.char = char
        self.xDir = 0
        self.yDir = 0
        self.range = 5
        self.active = True

    def getHealth(self):
        return self.health

    def setHealth(self, h):
        self.health = h

    def takeDamage(self, d):
        self.health -= d

    def setPos(self, x, y):
        self.xPos = x
        self.yPos = y

    def drawEnemy(self):
        if self.active:
            drawChar(self.xPos-1, self.yPos-1, self.health)
            drawChar(self.xPos, self.yPos, self.char)

    def checkPlayerDir(self, xPlayer, yPlayer):
        if self.xPos > xPlayer+1:
            self.xDir = -1
        elif self.xPos < xPlayer-1:
            self.xDir = 1
        else:
            self.xDir = 0

        if self.yPos > yPlayer+1:
            self.yDir = -1
        elif self.yPos < yPlayer-1:
            self.yDir = 1
        else:
            self.yDir = 0

    def checkPlayerDist(self, xPlayer, yPlayer):
        if math.dist((xPlayer, yPlayer), (self.xPos, self.yPos)) <= self.range:
            return True

    def checkPlayerAttack(self, xPlayer, yPlayer, direction, dmg):
        if self.active:
            if direction == "up":
                if xPlayer == self.xPos and yPlayer == (self.yPos + 1):
                    self.takeDamage(dmg)
                    if self.health <= 0:
                        self.active = False
                        return "KILLED,"+str(math.floor(self.baseHealth*self.hitChance*self.attack))
                    else:
                        return "HIT"
                else:
                    return "MISS"
            elif direction == "left":
                if xPlayer == (self.xPos + 1) and yPlayer == self.yPos:
                    self.takeDamage(dmg)
                    if self.health <= 0:
                        self.active = False
                        return "KILLED,"+str(math.floor(self.baseHealth*self.hitChance*self.attack))
                    else:
                        return "HIT"
                else:
                    return "MISS"
            elif direction == "down":
                if xPlayer == self.xPos and yPlayer == (self.yPos - 1):
                    self.takeDamage(dmg)
                    if self.health <= 0:
                        self.active = False
                        return "KILLED,"+str(math.floor(self.baseHealth*self.hitChance*self.attack))
                    else:
                        return "HIT"
                else:
                    return "MISS"
            elif direction == "right":
                if xPlayer == (self.xPos - 1) and yPlayer == self.yPos:
                    self.takeDamage(dmg)
                    if self.health <= 0:
                        self.active = False
                        return "KILLED,"+str(math.floor(self.baseHealth*self.hitChance*self.attack))
                    else:
                        return "HIT"
                else:
                    return "MISS"
            else:
                return False
        else:
            return "DEAD"

    def moveEnemy(self):
        self.xPos += self.xDir
        self.yPos += self.yDir
        self.drawEnemy()

    def checkActive(self):
        return self.active


class Player:
    """
    Class for the player, containing their attributes and main functions
    """
    posX = 5
    posY = 5
    health = 100
    score = 0
    damage = 50
    armour = 0
    inventory = {}
    attackChance = 0.33

    def __init__(self, name):
        self.name = name
        

    def drawPlayer(self):
        drawChar(self.posX, self.posY, "i")

    def damagePlayer(self, damage):
        self.health -= damage
        if self.health <= 0:
            end_game(self.score)

    def movePlayer(self, direction):
        if direction == "up":
            if self.posY > 1:
                self.posY -= 1

        elif direction == "down":
            if self.posY <= screenY-1:
                self.posY += 1

        elif direction == "left":
            if self.posX > 1:
                self.posX -= 1

        elif direction == "right":
            if self.posX <= screenX-1:
                self.posX += 1

    def getXPos(self):
        return self.posX

    def getYPos(self):
        return self.posY

    def getDamage(self):
        return self.damage
    
    def getAttackChance(self):
        return self.attackChance

    def setDamage(self, newDamage):
        self.damage = newDamage

    def addScore(self, amount):
        self.score += amount
    
    def getScore(self):
        return self.score

#Functions sourced from the internet


def inkey():
    """
    Retrieves the key which was pressed by the user without hitting
    enter.
    """
    fd=sys.stdin.fileno()
    remember_attributes=termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())
    character=sys.stdin.read(inkey_buffer)
    termios.tcsetattr(fd, termios.TCSADRAIN, remember_attributes)
    return character


#Function definitions


def drawChar(x, y, char):
    """
    Function to draw the specified character
    at a specific location in the terminal
    """

    print("\033["+str(y)+";"+str(x)+"f"+str(char))


def drawAscii(x, y, ascii):
    for i in range(0, len(ascii)):
        drawChar(x, y+i, ascii[i])

def generate_room(number):
    enemies = []
    for i in range(0, random.randint(1, number+1)):
        enemies.append(Enemy((10*(number)), 10, 0.2, random.randint(4, 79), random.randint(4, 23), "G"))

    return enemies
def start_menu():
    """
    Function to display the start menu
    """
    running = False
    os.system("clear")
    print(f.renderText("Into the Depths"))
    print("Please choose an option by typing either '1' or '2' and pressing enter. \n \n")
    print("1. Start Game")
    print("2. Instructions")
    choice = input("")

    while choice != "1" and choice != "2":
        print("Entered value: "+choice)
        print("Invalid choice, please type either '1' or '2' to make a selection")
        choice = input("")

    if choice == "1":
        start_game()
    elif choice == "2":
        display_instructions()


def getActiveEnemies(enemies):
    count = 0
    for e in enemies:
        if e.checkActive:
            count += 1
    return count

def start_game():
    """
    Main function to start the game
    """
    running = True
    P = Player("John")
    roomNo = 1
    roomClear = True
    message = ""
    playerTurn = True

    while running:
        enemyNo = 0

        if roomClear:
            enemies = generate_room(roomNo)
            #drawChar(1, 2, "Room generated")
            roomClear = False

        for e in enemies:
            if e.checkActive():
                enemyNo += 1
    
        if enemyNo == 0:
            message = "All enemies killed!"
            roomClear = True
            P.addScore(100 * roomNo)
            roomNo += 1

        os.system("clear")

        drawChar(1, 1, str(enemyNo)+" enemies remaining. - Player score is "+str(P.getScore())+" - "+message)

        P.drawPlayer()
        
        if not playerTurn:
            playerTurn = True
            for e in enemies:
                if e.checkActive():
                    if e.checkPlayerDist(P.getXPos(), P.getYPos()):
                        e.checkPlayerDir(P.getXPos(), P.getYPos())
                        e.moveEnemy()
                    else:
                        e.drawEnemy()
            ##inkey()
        else:
            for e in enemies:
                e.drawEnemy()

            char = inkey()
            playerTurn = False
        
            if char == chr(27):
                running = False
                start_menu()

            elif char == "w":
                P.movePlayer("up")
            elif char == "a":
                P.movePlayer("left")
            elif char == "s":
                P.movePlayer("down")
            elif char == "d":
                P.movePlayer("right")
            elif char == "i" or char == "j" or char == "k" or char == "l":
                if random.random() >= P.getAttackChance(): 
                    if char == "i":
                        attackDir = "up"
                    elif char == "j":
                        attackDir = "left"
                    elif char == "k":
                        attackDir = "down"
                    elif char == "l":
                        attackDir = "right"

                    for e in enemies:
                        attackResponse = e.checkPlayerAttack(P.getXPos(), P.getYPos(), attackDir, P.getDamage()).split(",")
                        if attackResponse[0] == "KILLED":
                            P.addScore(int(attackResponse[1]))
                            message = "Enemy killed"
                        elif attackResponse[0] == "HIT":
                            message = "Attack hit!"
                        elif attackResponse[0] == "MISS":
                            message = "Attack missed"
                        elif attackResponse[0] == "DEAD":
                            message = "Attack missed"
                        else:
                            message = "ERROR invalid attackResponse"
                else:
                    message = "Attack missed"


        #drawChar(15, 3, "Enemy's turn")
        #inkey()


def end_game(score):
    """
    Displays the 'game over' screen with the player's
    final score, giving the choice to return to
    the main menu or play again.
    """
    os.system("clear")
    running = False
    print(f.renderText("Game over") + "\n \n")
    print("""
    You have perished.
    Your final score was
        """ + str(score) +
        """
    Would you like to play again?
    Type 'y' to play again or 'n' to exit to the
    main menu.
        """)
    answer = input("")

    while answer != "y" and answer != "n":
        print("Entered value: "+answer)
        print("Invalid choice, please enter either 'y' or 'n' to make a selection.")
        answer = input("")

    if answer == "y":
        start_game()
    elif answer == "n":
        start_menu()


def display_instructions():
    """
    Display the game's instructions to the user
    """
    os.system("clear")
    print(f.renderText("Instructions") + "\n \n")
    print("Once you have started the game by choosing option '1' on the start menu,")
    print("you will be placed into the starting room where you can choose from a small")
    print("set of starting gear. If you are not happy with the choices presented, you")
    print("may re-roll for different options. Otherwise, make your choice and enter the")
    print("door to begin! \n")

    print("You will now battle your way through rooms which present harder and more")
    print("numerous enemies the further you go - finding more powerful items along the")
    print("way. The goal is to survive as long as you can and build up the highest")
    print("score possible. \n \n")

    input("Press enter for the game controls")

    os.system("clear")
    print(f.renderText("Controls") + "\n")
    print("Movement:")
    print("W - Up")
    print("A - Left")
    print("S - Down")
    print("D - Right \n")
    print("Attack:")
    print("I- Attack upwards")
    print("J - Attack left")
    print("K - Attack down")
    print("L - Attack right \n")
    print("Miscellaneous:")
    print("'i' - View inventory")
    print("'Esc' - Exit back to main menu \n")

    print(f.renderText("Good luck!"))


start_menu()
