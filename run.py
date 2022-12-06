#Imports

from pyfiglet import Figlet
import colorama
import os
import termios
import sys
import tty

#Variable declarations
f = Figlet(font="slant")
screenX = 80
screenY = 24
inkey_buffer = 1
current_level = 1


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


class Player:
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

def start_menu():
    """
    Function to display the start menu
    """

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
    while running:
        os.system("clear")

        drawAscii(5, 5, doorOpenAscii)

        drawChar(1, 1, "Player pos: X: "+str(P.getXPos())+ " Y: "+str(P.getYPos()))
        P.drawPlayer()
        char = inkey()
        

        #print("DEBUG: key '" + char + "' was pressed")
        if char == chr(27):
            start_menu()

        elif char == "w":
            P.movePlayer("up")
        elif char == "a":
            P.movePlayer("left")
        elif char == "s":
            P.movePlayer("down")
        elif char == "d":
            P.movePlayer("right")
        elif char == "b":
            drawChar(P.getXPos(), P.getYPos(), boxEmptyAscii)
        
def end_game(score):
    """
    Displays the 'game over' screen with the player's
    final score, giving the choice to return to
    the main menu or play again.
    """
    os.system("clear")

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
    print("'i' - View inventory \n")

    print(f.renderText("Good luck!"))


start_menu()