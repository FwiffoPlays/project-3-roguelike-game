# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

from pyfiglet import Figlet
import colorama
import os


def start_menu():
    f = Figlet(font='slant')
    os.system('clear')
    print(f.renderText('Into the Depths'))
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
    print("Instructions:")

start_menu()