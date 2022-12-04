# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

from pyfiglet import Figlet
import colorama
import os


f = Figlet(font="slant")

def start_menu():
    
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
    print("Game started!")

def display_instructions():
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