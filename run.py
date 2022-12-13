#Imports

from pyfiglet import Figlet
import colorama
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
    def __init__(self, health, damage, hitChance, xPos, yPos, char):
        self.health = health
        self.damage = damage
        self.hitChance = hitChance
        self.xPos = xPos
        self.yPos = yPos
        self.char = char
        self.xDir = 0
        self.yDir = 0
        self.range = 5

    def getHealth(self):
        return self.health

    def setHealth(self, h):
        self.health = h

    def damage(self, d):
        self.health -= d

    def setPos(self, x, y):
        self.xPos = x
        self.yPos = y

    def drawEnemy(self):
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

    def moveEnemy(self):
        self.xPos += self.xDir
        self.yPos += self.yDir
        self.drawEnemy()


class Player:
    """
    Class for the player, containing their attributes and main functions
    """
    posX = 1
    posY = 1
    health = 100
    score = 10
    armour = 0
    inventory = {}

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


def start_game():
    """
    Main function to start the game
    """
    running = True
    P = Player("John")
    roomNo = 1
    roomClear = True
    

    while running:

        if roomClear:
            enemies = generate_room(roomNo)
            drawChar(1, 2, "Room generated")
            roomClear = False

        os.system("clear")

        #drawAscii(5, 5, doorOpenAscii)

        #drawChar(1, 1, "DEBUG Player pos: X: "+str(P.getXPos())+ " Y: "+str(P.getYPos()))
        drawChar(1, 1, str(len(enemies))+" enemies remaining")

        P.drawPlayer()

        #inkey()
        #inkey()
        for e in enemies:
            if e.checkPlayerDist(P.getXPos(), P.getYPos()):
                e.checkPlayerDir(P.getXPos(), P.getYPos())
                e.moveEnemy()
            else:
                e.drawEnemy()
        #drawChar(3, 1, "Debug: ")
        char = inkey()

        #print("DEBUG: key '" + char + "' was pressed")
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
    print("Up arrow - Attack upwards")
    print("Left arrow - Attack left")
    print("Down arrow - Attack down")
    print("Right arrow - Attack right \n")
    print("Miscellaneous:")
    print("'i' - View inventory")
    print("'Esc' - Exit back to main menu \n")

    print(f.renderText("Good luck!"))


start_menu()
