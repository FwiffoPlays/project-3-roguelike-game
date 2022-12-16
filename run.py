"""
Code Institute Project 3 - Python Essentials
This is a terminal-based roguelike game where the player
strives to get the highest score possible by killing
progressively more difficult waves of enemies.
"""
# Imports


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
        """
        Returns the enemy's current health
        """
        return self.health

    def set_health(self, new_health):
        """
        Sets the enemy's health to the provided value
        """
        self.health = new_health

    def take_damage(self, dam):
        """
        Decreases the enemy's health by the provided value
        """
        self.health -= dam

    def set_pos(self, x_val, y_val):
        """
        Sets the enemy's health to the provided x and y values
        """
        self.x_pos = x_val
        self.y_pos = y_val

    def draw_enemy(self):
        """
        Draws the current enemy's character if they are alive/active
        """
        if self.active:
            draw_char(self.x_pos-1, self.y_pos-1, self.health)
            draw_char(self.x_pos, self.y_pos, self.char)

    def check_player_dir(self, x_player, y_player):
        """
        Sets which direction the enemy must move to approach the player
        """
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

    def check_player_range(self, x_player, y_player):
        """
        Checks whether the player is in visual range of the enemy
        """
        if math.dist(
                    (x_player, y_player),
                    (self.x_pos, self.y_pos)) <= self.range:
            return True

    def check_player_dist(self, x_player, y_player):
        """
        Checks if the player is close enough to attack
        """
        if math.dist(
                    (x_player, y_player),
                    (self.x_pos, self.y_pos)) == 1:
            return True

    def attempt_attack(self):
        """
        Decides if the enemy's attack on the player was successful
        """
        if random.random() <= self.hit_chance:
            return self.attack
        else:
            return False

    def check_player_attack(self, x_player, y_player, direction, dmg):
        """
        Checks if the player's attack hits and returns the enemy's new status
        depending on the result
        """
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
        """
        Moves the enemy towards the player
        """
        self.x_pos += self.x_dir
        self.y_pos += self.y_dir
        self.draw_enemy()

    def check_active(self):
        """
        Returns the enemy's state (alive/dead)
        """
        return self.active


class Player:
    """
    Class for the player, containing their attributes and main functions
    """
    pos_x = 5
    pos_y = 5
    health = 100
    score = 0
    damage = 50
    armour = 0
    inventory = {}
    attack_chance = 0.33

    def __init__(self, name):
        self.name = name

    def draw_player(self):
        """
        Draws the player's character at the player's position
        """
        draw_char(self.pos_x, self.pos_y, "i")

    def damage_player(self, damage):
        """
        Reduces the player's health by the provided amount and checks
        whether they are still alive, ending the game if not
        """
        self.health -= damage
        if self.health <= 0:
            end_game(self.score)

    def move_player(self, direction):
        """
        Moves the player in the provided direction
        """
        if direction == "up":
            if self.pos_y > 1:
                self.pos_y -= 1

        elif direction == "down":
            if self.pos_y <= SCREENY-1:
                self.pos_y += 1

        elif direction == "left":
            if self.pos_x > 1:
                self.pos_x -= 1

        elif direction == "right":
            if self.pos_x <= SCREENX-1:
                self.pos_x += 1

    def get_x_pos(self):
        """
        Returns the player's x coordinate
        """
        return self.pos_x

    def get_y_pos(self):
        """
        Returns the player's y coordinate
        """
        return self.pos_y

    def get_damage(self):
        """
        Returns the player's damage stat
        """
        return self.damage

    def get_health(self):
        """
        Returns the player's health
        """
        return self.health

    def get_attack_chance(self):
        """
        Returns the player's hit chance stat
        """
        return self.attack_chance

    def set_damage(self, new_damage):
        """
        Sets the player's damage stat to the provided value
        """
        self.damage = new_damage

    def add_score(self, amount):
        """
        Increases the player's score by the provided amount
        """
        self.score += amount

    def get_score(self):
        """
        Returns the player's score
        """
        return self.score

# Functions sourced from the internet


def inkey():
    """
    Retrieves the key which was pressed by the user without hitting
    enter. Sourced from:
    https://code.activestate.com/recipes/577728-simpletron3xpy-game-to-demo-xy-drawing-using-the-k/?in=user-4177147
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


def generate_room(number):
    """
    Randomly generates a set of enemies based on the current level/room
    number
    """
    enemies = []
    for i in range(0, random.randint(1, number+1)):
        enemies.append(
            Enemy(
                10 * (number),
                10,
                0.1 * (number),
                random.randint(4, 79),
                random.randint(4, 23),
                "G")
            )
    return enemies


def start_menu():
    """
    Function to display the start menu
    """
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
    """
    Returns the number of enemies still alive
    """
    count = 0
    for enemy in enemies:
        if enemy.check_active:
            count += 1
    return count


def start_game():
    """
    Main function to start the game, containing the main loop and
    logic for player movement
    """
    running = True
    player = Player("John")
    room_no = 1
    room_clear = True
    message = ""
    player_turn = True

    while running:
        enemy_no = 0

        if room_clear:
            enemies = generate_room(room_no)
            room_clear = False

        for enemy in enemies:
            if enemy.check_active():
                enemy_no += 1

        if enemy_no == 0:
            message = "All enemies killed!"
            room_clear = True
            player.add_score(100 * room_no)
            room_no += 1

        os.system("clear")

        draw_char(1, 1, str(enemy_no) +
                  " enemies remaining. - Player score is " +
                  str(player.get_score()) + " - " +
                  "Health: " + str(player.get_health()) + " - " +
                  message)

        player.draw_player()

        if not player_turn:
            player_turn = True

            for enemy in enemies:
                if enemy.check_active():
                    if enemy.check_player_dist(player.get_x_pos(),
                                               player.get_y_pos()):
                        attack_damage = enemy.attempt_attack()
                        if attack_damage:
                            player.damage_player(attack_damage)
                    else:
                        if enemy.check_player_range(player.get_x_pos(),
                                                    player.get_y_pos()):
                            enemy.check_player_dir(player.get_x_pos(),
                                                   player.get_y_pos())
                            enemy.move_enemy()
                        else:
                            enemy.draw_enemy()
        else:
            for enemy in enemies:
                enemy.draw_enemy()

            char = inkey()
            player_turn = False

            if char == chr(27):
                running = False
                start_menu()

            elif char == "w":
                player.move_player("up")
            elif char == "a":
                player.move_player("left")
            elif char == "s":
                player.move_player("down")
            elif char == "d":
                player.move_player("right")
            elif char == "i" or char == "j" or char == "k" or char == "l":
                if random.random() >= player.get_attack_chance():
                    if char == "i":
                        attack_dir = "up"
                    elif char == "j":
                        attack_dir = "left"
                    elif char == "k":
                        attack_dir = "down"
                    elif char == "l":
                        attack_dir = "right"

                    for enemy in enemies:
                        attack_response = enemy.check_player_attack(
                                                            player.get_x_pos(),
                                                            player.get_y_pos(),
                                                            attack_dir,
                                                            player.get_damage()
                                                            ).split(",")
                        if attack_response[0] == "KILLED":
                            player.add_score(int(attack_response[1]))
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


def end_game(score):
    """
    Displays the 'game over' screen with the player's
    final score, giving the choice to return to
    the main menu or play again.
    """
    os.system("clear")

    print(f.renderText("Game over") + "\n \n")
    print("You have perished. \nYour final score was " +
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
          "you will be placed into the first room, containing " +
          "enemies for you to fight, represented by a 'G'. " +
          "\nThe number above each enemy is their current health."
          "\nWhen all enemies are defeated " +
          "you will move onto the next room containing more enemies." +
          "\nThe number of enemies and their stats (such as" +
          " health and attack chance) will increase as you progress " +
          "through the game, increasing difficulty.\n" +
          "If your health reaches zero, the game is over " +
          "and you will be told your final score, with the option " +
          "to either play again or exit to the main menu.")

    input("\nPress enter for the game controls")

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
    print("'Esc key' or 'Arrow keys' - Exit back to main menu \n")

    print(f.renderText("Good luck!"))

    input("Press enter to return to the main menu")
    start_menu()


start_menu()
