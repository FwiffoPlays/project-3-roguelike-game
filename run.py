# Imports


# import colorama
import os
import termios
import sys
import tty
import math
import random

from pyfiglet import Figlet

# Variable declarations

f = Figlet(font="slant")
SCREENX = 80
SCREENY = 24
INKEY_BUFFER = 1
# running = False

# Ascii art

box_full_ascii = [
    "+---+",
    "| i |",
    "+---+"
]

box_empty_ascii = [
    "+---+",
    "|   |",
    "+---+"
]

door_closed_ascii = [
    "+--+",
    "||||",
    "||||",
    "+--+"
]

door_open_ascii = [
    "+--+",
    "|  |",
    "|  |",
    "+--+"
]


# Class definitions


class Enemy:
    """
    Generic class for enemies, defining their variables and functions
    """
    def __init__(self, base_health, attack, hit_chance, x_pos, y_pos, char):
        self.base_health = base_health
        self.health = base_health
        self.attack = attack
        self.hit_chance = hit_chance
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.char = char
        self.x_dir = 0
        self.y_dir = 0
        self.range = 5
        self.active = True

    def get_health(self):
        return self.health

    def set_health(self, new_health):
        self.health = new_health

    def take_damage(self, dam):
        self.health -= dam

    def set_pos(self, x_val, y_val):
        self.x_pos = x_val
        self.y_pos = y_val

    def draw_enemy(self):
        if self.active:
            draw_char(self.x_pos-1, self.y_pos-1, self.health)
            draw_char(self.x_pos, self.y_pos, self.char)

    def check_player_dir(self, x_player, y_player):
        if self.x_pos > x_player+1:
            self.x_dir = -1
        elif self.x_pos < x_player-1:
            self.x_dir = 1
        else:
            self.x_dir = 0

        if self.y_pos > y_player+1:
            self.y_dir = -1
        elif self.y_pos < y_player-1:
            self.y_dir = 1
        else:
            self.y_dir = 0

    def check_player_dist(self, x_player, y_player):
        if math.dist(
                    (x_player, y_player),
                    (self.x_pos, self.y_pos)) <= self.range:
            return True

    def check_player_attack(self, x_player, y_player, direction, dmg):
        if self.active:
            if direction == "up":
                if x_player == self.x_pos and y_player == (self.y_pos + 1):
                    self.take_damage(dmg)
                    if self.health <= 0:
                        self.active = False
                        return ("KILLED," +
                                str(math.floor(
                                    self.base_health *
                                    self.hit_chance *
                                    self.attack)
                                    )
                                )
                    else:
                        return "HIT"
                else:
                    return "MISS"
            elif direction == "left":
                if x_player == (self.x_pos + 1) and y_player == self.y_pos:
                    self.take_damage(dmg)
                    if self.health <= 0:
                        self.active = False
                        return "KILLED," + str(
                                               math.floor(
                                                          self.base_health *
                                                          self.hit_chance *
                                                          self.attack)
                                              )
                    else:
                        return "HIT"
                else:
                    return "MISS"
            elif direction == "down":
                if x_player == self.x_pos and y_player == (self.y_pos - 1):
                    self.take_damage(dmg)
                    if self.health <= 0:
                        self.active = False
                        return "KILLED," + str(
                                               math.floor(
                                                          self.base_health *
                                                          self.hit_chance *
                                                          self.attack)
                                              )
                    else:
                        return "HIT"
                else:
                    return "MISS"
            elif direction == "right":
                if x_player == (self.x_pos - 1) and y_player == self.y_pos:
                    self.take_damage(dmg)
                    if self.health <= 0:
                        self.active = False
                        return "KILLED," + str(
                                               math.floor(
                                                          self.base_health *
                                                          self.hit_chance *
                                                          self.attack)
                                              )
                    else:
                        return "HIT"
                else:
                    return "MISS"
            else:
                return False
        else:
            return "DEAD"

    def move_enemy(self):
        self.x_pos += self.x_dir
        self.y_pos += self.y_dir
        self.draw_enemy()

    def check_active(self):
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
    attack_chance = 0.33

    def __init__(self, name):
        self.name = name

    def draw_player(self):
        draw_char(self.posX, self.posY, "i")

    def damage_player(self, damage):
        self.health -= damage
        if self.health <= 0:
            end_game(self.score)

    def move_player(self, direction):
        if direction == "up":
            if self.posY > 1:
                self.posY -= 1

        elif direction == "down":
            if self.posY <= SCREENY-1:
                self.posY += 1

        elif direction == "left":
            if self.posX > 1:
                self.posX -= 1

        elif direction == "right":
            if self.posX <= SCREENX-1:
                self.posX += 1

    def getx_pos(self):
        return self.posX

    def gety_pos(self):
        return self.posY

    def get_damage(self):
        return self.damage

    def get_attack_chance(self):
        return self.attack_chance

    def set_damage(self, newDamage):
        self.damage = newDamage

    def add_score(self, amount):
        self.score += amount

    def get_score(self):
        return self.score

# Functions sourced from the internet


def inkey():
    """
    Retrieves the key which was pressed by the user without hitting
    enter.
    """
    fd = sys.stdin.fileno()
    remember_attributes = termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())
    character = sys.stdin.read(INKEY_BUFFER)
    termios.tcsetattr(fd, termios.TCSADRAIN, remember_attributes)
    return character


# Function definitions


def draw_char(x_pos, y_pos, char):
    """
    Function to draw the specified character
    at a specific location in the terminal
    """

    print("\033["+str(y_pos)+";"+str(x_pos)+"f"+str(char))


def draw_ascii(x_pos, y_pos, ascii_list):
    for i in range(0, len(ascii_list)):
        draw_char(x_pos, y_pos+i, ascii_list[i])


def generate_room(number):
    enemies = []
    for i in range(0, random.randint(1, number+1)):
        enemies.append(
            Enemy(
                (10 * (number)),
                10,
                0.2,
                random.randint(4, 79),
                random.randint(4, 23),
                "G")
            )
    return enemies


def start_menu():
    """
    Function to display the start menu
    """
    # running = False
    os.system("clear")
    print(f.renderText("Into the Depths"))
    print("Please choose an option by typing either" +
          "'1' or '2' and pressing enter. \n \n")
    print("1. Start Game")
    print("2. Instructions")
    choice = input("")

    while choice != "1" and choice != "2":
        print("Entered value: "+choice)
        print("Invalid choice, please type either " +
              "'1' or '2' to make a selection")
        choice = input("")

    if choice == "1":
        start_game()
    elif choice == "2":
        display_instructions()


def get_active_enemies(enemies):
    count = 0
    for e in enemies:
        if e.check_active:
            count += 1
    return count


def start_game():
    """
    Main function to start the game
    """
    running = True
    P = Player("John")
    room_no = 1
    room_clear = True
    message = ""
    player_turn = True

    while running:
        enemy_no = 0

        if room_clear:
            enemies = generate_room(room_no)
            # draw_char(1, 2, "Room generated")
            room_clear = False

        for e in enemies:
            if e.check_active():
                enemy_no += 1

        if enemy_no == 0:
            message = "All enemies killed!"
            room_clear = True
            P.add_score(100 * room_no)
            room_no += 1

        os.system("clear")

        draw_char(1, 1, str(enemy_no) +
                  " enemies remaining. - Player score is " +
                  str(P.get_score()) + " - " + message)

        P.draw_player()

        if not player_turn:
            player_turn = True
            for e in enemies:
                if e.check_active():
                    if e.check_player_dist(P.getx_pos(), P.gety_pos()):
                        e.check_player_dir(P.getx_pos(), P.gety_pos())
                        e.move_enemy()
                    else:
                        e.draw_enemy()
            # inkey()
        else:
            for e in enemies:
                e.draw_enemy()

            char = inkey()
            player_turn = False

            if char == chr(27):
                running = False
                start_menu()

            elif char == "w":
                P.move_player("up")
            elif char == "a":
                P.move_player("left")
            elif char == "s":
                P.move_player("down")
            elif char == "d":
                P.move_player("right")
            elif char == "i" or char == "j" or char == "k" or char == "l":
                if random.random() >= P.get_attack_chance():
                    if char == "i":
                        attack_dir = "up"
                    elif char == "j":
                        attack_dir = "left"
                    elif char == "k":
                        attack_dir = "down"
                    elif char == "l":
                        attack_dir = "right"

                    for e in enemies:
                        attack_response = e.check_player_attack(
                                                             P.getx_pos(),
                                                             P.gety_pos(),
                                                             attack_dir,
                                                             P.get_damage()
                                                             ).split(",")
                        if attack_response[0] == "KILLED":
                            P.add_score(int(attack_response[1]))
                            message = "Enemy killed"
                        elif attack_response[0] == "HIT":
                            message = "Attack hit!"
                        elif attack_response[0] == "MISS":
                            message = "Attack missed"
                        elif attack_response[0] == "DEAD":
                            message = "Attack missed"
                        else:
                            message = "ERROR invalid attack_response"
                else:
                    message = "Attack missed"

        # draw_char(15, 3, "Enemy's turn")
        # inkey()


def end_game(score):
    """
    Displays the 'game over' screen with the player's
    final score, giving the choice to return to
    the main menu or play again.
    """
    os.system("clear")
    # running = False
    print(f.renderText("Game over") + "\n \n")
    print("You have perished. \nYour final score was" +
          str(score) +
          "\nWould you like to play again?\n" +
          "Type 'y' to play again or 'n' to exit to the main menu.")
    answer = input("")

    while answer != "y" and answer != "n":
        print("Entered value: "+answer)
        print("Invalid choice, please enter either 'y' " +
              "or 'n' to make a selection.")
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
    print("Once you have started the game by choosing " +
          "option '1' on the start menu, " +
          "you will be placed into the starting room " +
          "where you can choose from a small"
          "set of starting gear. If you are not happy " +
          "with the choices presented, you" +
          "may re-roll for different options. Otherwise, " +
          "make your choice and enter the" +
          "door to begin! \n\n" +
          "You will now battle your way through rooms " +
          "which present harder and more" +
          "numerous enemies the further you go - " +
          "finding more powerful items along the" +
          "way. The goal is to survive as long as " +
          "you can and build up the highest" +
          "score possible. \n \n")

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
