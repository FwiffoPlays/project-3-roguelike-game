# Into the Depths - Project 3

Into the Depths is a Python based command-line game for Project 3 of the Code Insitute Full Stack Web Development course.

It is based on the 'roguelike' genre of games and utilises ASCII art in the command line as visual feedback for the user.

The deployed code can be found [here](https://ci-project-3-roguelike-game.herokuapp.com/)

## How To Play

Once the game is launched the user is first presented with the main menu where they may choose either from two options by entering either '1' or '2' as an input. '1' being 'Start Game' and '2' Being 'Instructions'.

The 'Instructions' option presents the user with mainly the same information included here, listing the purpose of the game and various controls, whilst the 'Start Game' option begins the main game.

The objective of the game is to navigate through a set of room or dungeons with progressively more difficult enemies to defeat to see how long the player can survive. As they play the game a 'score' is tallied up for actions such as killing an enemy or finishing a room which the player is shown upon the game ending.

The controls are as follows:

The W, A, S, D keys move the player Up, Left, Down or Right respectively
The I, J, K and L keys attack in their respective directions.
The 'Esc' key or Arrow keys exit the game back to the main menu. 

## Features

**Start menu**

* This is the first screen the player is presented with when starting the game. The game's name is displayed at the top using the Pyfiglet library and the user is presented with the choice of either 1: starting the game or 2: reading the instructions.
* The game then waits for an input where the user must type either '1' or '2'. Any other input will output an error to the user, reminding them to type either '1' or '2' to make a selection.

![Start menu screenshot](assets/images/readme/StartMenu.png)

**Main game**

* Below is an example screenshot of the main game loop, which begins once the user enters '1' on the start menu.
* The player character, 2 enemies and the information panel are visible here, which are individual features of the game which will be explained further down.
* Once the player has killed all enemies on the screen, the room number increases and the new room is generated.

![Main game screenshot](assets/images/readme/MainGame.png)

**Instructions page**

* If the user types '2' on the start menu, they are then presented with the following instructions page.
* Here, the game's objective is displayed on the first page. The program will then wait for the user to press enter before moving onto the second page.

![Instructions page 1 screenshot](assets/images/readme/Instructions1.png)

* The second page tells the user the game's controls, again waiting for enter to be pressed before returning to the main menu.

![Instructions page 2 screenshot](assets/images/readme/Instructions2.png)

**Player character**

* The player's character is represented by an 'i'. As stated in the instructions, they are able to move around using the 'W', 'A', 'S' and 'D' keys, as well as attack using the 'I', 'J', 'K' and 'L' keys. Any of these actions will end the player's turn, allowing the enemy to immediately take theirs.
* When within the range of 1 'char' or letter of an enemy, they may attempt an attack using the attack keys in the direction of the enemy. In this version of the game the player has a fixed hit chance of 33%.

![Player character screenshot](assets/images/readme/Player.png)

**Enemies**

* Enemies are represented by the letter 'G' and have their current health displayed above them. When within visual range of the player (currently fixed to 5 characters) they will move towards them when it is their turn and if they are one character away will attempt an attack.
* They are randomly generated by the 'generate_room' method which uses the 'Enemy' class. Their health and hit chance scale up based on the current room number, increasing their difficulty as the player progresses through the game.

![Enemy screenshot](assets/images/readme/Enemy.png)

**Information panel**

* The information panel is displayed at the top of the screen throughout gameplay and provides feedback to the player, such as telling them the remaining number of enemies; their health; their current score and the outcome of recent actions such as attacks or killing enemies.
* This aids the player in understanding their progress in the game and important information such as their health, improving the user experience.

![Information panel screenshot](assets/images/readme/InfoPanel.png)

**Game over**

* Once the player's health reaches zero, they are presented with the 'Game Over' screen where they are told their final score, as well as given the option to type 'y' to play again or 'n' to return to the main menu.
* This allows the player to keep track of what scores they have achieved, adding a sense of replayability as they compete with themselves or others for a higher score.

![Game over screenshot](assets/images/readme/GameOver.png)

### Future development and features

* Adding randomly generated items for the player to pick up which will aid them by increasing stats or allowing for actions such as healing. Having a limited inventory capacity for such items would introduce the additional aspect of inventory management, adding further depth to the gameplay.

## Flow Control

* The following flow control diagram shows the initial plan for the game's logic, which aided in development when considering each part of the game and they would interact with eachother.
* Due to time constraints certain features were ommitted for the final release, which will be detailed below.

![Flow control diagram](assets/images/readme/FlowControlDiagram.jpg)

* Entering the user's name, the starting room to select initial gear and collecting items throughout the game were the main 3 features which did not make it to the final release. With more time, adding these features (particularly collecting items) would add to the progression and user experience of the game and so would be main goals for a potential future release.

## Aesthetic Design

* The game features a simple aesthetic design, making use of ASCII symbols such as the 'i' to represent the player.
* The 'Pyfiglet' library was used to emphasise pieces of text during the game's menus by turning them into ASCII art, making them stand out to the player.

![PyFiglet ASCII art example screenshot](assets/images/readme/ASCIIArtExample.png)

### Future aesthetic changes

* My original plan for the game involved using the 'colorama' library to add colour to elements of the game, which would have made it easier for the player to differentiate between objects in the game, as well as provided an additional layer of visual feedback to the player, improving the game's general playability as well as the user experience.

## Libraries and Technology Used

**Built-in Libraries**

**os**
* The 'OS' library provides functions for interacting with the Operating System, such as clearing the terminal the code is running in, as it is used in this project.

math
* Provides various useful maths operations
* This was mainly used for the 'math.floor' function to round down a number.

random
* Includes various forms of random number generation
* This was used to add elements of randomness to the game, such as enemy generation.

termios
* Provides UNIX-specific terminal controls (This project was developed on and runs within a UNIX based terminal)
* This was used for the method sourced from the internet for getting the character the user pressed

sys
* This was used for the method sourced from the internet for getting the character the user pressed

tty
* This was used for the method sourced from the internet for getting the character the user pressed

**Third-party Libraries**

**pyfiglet**
* PyFiglet is a third-party library which allows for the easy creation of ASCII-Art text

**Other technologies used**

* Heroku was used as cloud app host to deploy the final project
* Gitpod was the main development environment which allowed for the project to be easily worked on usin any computer with an internet connection and a web browser.

## Testing

* During various stages of development I used techniques such as printing variable value and eventually using my 'drawChar' method to allow me to debug certain values as the program ran.

* All errors and most warnings were fixed using the feedback provided by the Python linter and Visual Studio Code, which ensures the code will run without syntax errors and remain readable for future development.

* All forms of input within the game were tested throughout development to make sure they both responded to valid inputs as expected and handled incorrect inputs in a graceful way, such as providing feedback to the user to remind them of the valid input choices. 

    * The start menu accepts only '1' or '2' as inputs and responds with a prompt for either of these values if anything else is entered.

    * The instructions pages will accept any input value, as long as 'enter' is pressed by the user to continue. The input value received by the user is not stored as it is not required here so any input is allowed.

    * The game over method accepts only 'y' or 'n' as responses and also prompts for these values if anything else is entered by the user.

    * The main game's inputs were tested to ensure they work as intended ('W', 'A', 'S' and 'D' keys move 'Up', 'Left', 'Down' and 'Right' as expected. The 'I', 'J', 'K' and 'L' keys also attack in their respective directions.) The escape key returns the player to the main menu as expected. Pressing most other keys on the keyboard results in no action as expected, however pressing any key which uses 'escape' character in the terminal (such as the arrow keys or function keys) will also exit the user to the main menu as these are all interpreted as 'escape' characters.

 * In gameplay the player is able to attack successfully, as well as the enemies being able to chase and attack the player. Both the player and enemies can take damage and die.

 * The 'Game Over' screen is correctly triggered when the player's health reached zero, which also output the player's score as intended.

### Found issues/bugs

* Pressing any key which sends 'escape' characters to the terminal (such as 'Esc' or function keys) will return to the main menu, however only the 'Esc' key was intended to be able to do this. This could be solved by looking at all the characters a key sends to the terminal, as each of these keys produces their own escape character code (For example 'Esc' is just '^[' whereas the 'Up' arrow key is '^[[A')

* The information panel at the top of the game will sometimes show incorrect status messages, such as displaying 'Attack missed' despite a player's attack hitting an enemy. This could be resolved by reviewing the logic involved in producing these messages to ensure only the correct ones are displayed.

### Validator testing

* The Code Institute Python Linter tool was used to verify that my python code followed the naming and formatting conventions for python. This was done by copying and pasting my code into the tester, which confirmed no errors as shown below:
![Screenshot of the results from the Code Institude Python Linter tool](assets/images/readme/CIPythonLinterResult.png)

## Deployment

The project was deployed to [Heroku](https://dashboard.heroku.com/apps), which is a cloud application platform that allows developers to host their projects on the Heroku servers which will run their apps.

The Code Institute Python Essentials template was used to provide an emulated terminal to allow the project to be deployed and used within Heroku as if it was being ran straight from a Linux terminal locally.

The command 'pip3 freeze > requirements.txt' must be typed before beginning deployment so that Heroku knows which third party libraries it needs to install for the project.

Heroku deployment was done as follows:

1. Login or sign up to Heroku
2. Click 'New' on the main dashboard in the top right and then click 'Create New App' in the drop down.
3. Enter a unique name for the app (This project uses 'ci-project-3-roguelike-game')
4. Select the region applicable for you
5. Click 'Create App'
6. Go to the 'Settings' tab and add the 'Python' and 'Node.JS' buildpacks under the 'Buildpacks' section, ensuring the Python pack comes before (is on top of) the Node.JS pack.
7. Open the 'Deploy' tab at the top of the page
8. Click 'Github' to use as the deployment method
9. Authorise the connection to GitHub
10. Type your repository's name to search for it and click 'Connect'
11. At the bottom choose the 'Deploy Branch' option (The 'Enable Automatic Deployment' option is also recommended for easier updates when you make changes to your project)


### Version Control

Throughout the sites development, the version control system 'Git' was used to upload code changes. The following commands were written into the command line to perform this for each change:

git add <file> -Tells git which file(s) should be added to the next commit. ('git add .' includes all files and folders in the current directory, which was used for most of the project's development so that changes such as adding images to the readme were also included.)

git commit -m "Commit message" -Creates a commit with the added files and sets the commit log message.

git push -Sends the commit to the Git server for backup

## Credits

The 'inkey' method used for getting the key the user has pressed in a terminal without them pressing enter was sourced from the program here which provided a simple demo of it:
    https://code.activestate.com/recipes/577728-simpletron3xpy-game-to-demo-xy-drawing-using-the-k/?in=user-4177147