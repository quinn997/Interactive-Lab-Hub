# Final Project

Using the tools and techniques you learned in this class, design, prototype and test an interactive device.

Project Github page set up - May 3

Functional check-off - May 10
 
Final Project Presentations (video watch party) - May 12

Final Project Documentation due - May 19



## Objective

The goal of this final project is for you to have a fully functioning and well-designed interactive device of your own design.
 
## Description
Your project is to design and build an interactive device to suit a specific application of your choosing. 

## Deliverables

1. Documentation of design process
2. Archive of all code, design patterns, etc. used in the final design. (As with labs, the standard should be that the documentation would allow you to recreate your project if you woke up with amnesia.)
3. Video of someone using your project (or as safe a version of that as can be managed given social distancing)
4. Reflections on process (What have you learned or wish you knew at the start?)


## Teams

You can and are not required to work in teams. Be clear in documentation who contributed what. The total project contributions should reflect the number of people on the project.

## Examples

[Here is a list of good final projects from previous classes.](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/wiki/Previous-Final-Projects)
This version of the class is very different, but it may be useful to see these.


----------------------------------

# Final Project - Game: Deal Or No Deal

----------------------------------

## Team Members: Andrew Liu (jl3983), Quinn Wu (yw2325)

----------------------------------

## Table Of Contents:

----------------------------------

- [Game Description](#game-description)
- [Software Design](#software-design)
- [Prototype Design](#prototype-design)
- [Final Video](#final-video)
- [Reflections](#reflections)

----------------------------------

### Game Description

Deal Or No Deal is a kind of television game show, which is played with up to 26 cases, each containing randomly assigned sums of money. The player claims one case at the start of the game, without its money value being revealed. The player then chooses the other cases, one at a time, to be immediately opened and removed from play. Throughout the game, the player is offered an amount of money or prizes to quit, being asked the question, "Deal or no deal?" If the player rejects every deal and eliminates all the other cases, the player keeps the money that was in the original case. Thus, the player "wins" depending on whether the player should have taken one of the deals or should have held onto the original case until the very end.

----------------------------------

### Software Design

There are two important parts in software design: game logics and user interface.

#### Game Logics:

The original version of the game, Deal Or No Deal, is played with 26 cases. Since the game is designed to use Raspberry Pi, there are two options available: using the SparkFun Qwiic Thumb Joystick or Adafruit MPR121 12-Key Capacitive Touch Sensor to select the cases. However, if the game contains 26 cases, we can only use the joystick. After we tested its performance, we found the user experience was bad because it was hard to switch between the cases (slow, inaccurate controlling, etc.). And we decided to use two capacitive sensors which had 24 keys available. Therefore, we modified the game and it was played with 24 cases. 

In order to realize the game logics, first, we created a list which contains 24 money values: $0.01, $1, $5, $10, $25, $50, $75, $100, $200, $300, $500, $750, $1000, $5000, $25000, $50000, $75000, $100000, $200000, $300000, $400000, $500000, $750000, $1000000. Second, shuffled these values randomly and assigned them to 24 “cases” (using the index of each value in the list as the case number). The player will select a “case”, and we will mark the corresponding money value unavailable. Then, the player will choose 6 “cases”, one at a time, and we will reveal the money value in each “case” immediately after each one. After that, a bank offer will be provided. If the player chooses “Deal” by pressing the SparkFun Qwiic Green Button (green_button.is_button_pressed() == True), the game is over, and the player takes the money being offered. If the player chooses “No Deal” by pressing the SparkFun Qwiic Red Button (red_button.is_button_pressed() == True), the game will continue, and the player will select 5 “cases”, 4 “cases”,  3 “cases”, 2 “cases”, 1 “case”, and 1 “case” (in such an order). Again, the money value will be revealed immediately after each “case” they select, and a bank offer will be provided in between.

The bank offer formula:

    money offered = ( the total amount of money in the remaining cases / the number of remaining cases ) * (round number of the game / 10)

The game is over when the player presses the green button to accept the bank offer or when the player plays till the end. All the money values will be displayed.

#### User Interface:

Instead of displaying all the information (money values, prompt messages, case numbers, etc.) in the terminal, an UI with images and soundtracks will instill a sense of control in the player. So, the player can quickly learn and gain a fast sense of mastery. There are two modules which can be used to create the UI, “Pygame” and “Tkinter”. They are similar in some respects (creating frames, modifying frames, updating frames, etc.). We decided to use “Tkinter” since it is packaged with Python, and there is no need to install other dependency libraries which may cause unpredictable problems in the future. We also considered using “MQTT” to achieve remote control. But as we learned from lab 6, using the “client-server” architecture will cause a noticeable delay during the game play, which makes the player uncomfortable. Therefore, we gave up this idea, and the game would run on a single Raspberry Pi. The images of cases are placed in the center, and the images of money values are placed on both sides with smaller ones on the left and larger ones on the right. We developed Harmehar Singh's project (Github link: https://github.com/SinghHarmehar/Deal-No-Deal), credit to its good images and frame design. In order to highly restore the original game, we also added the soundtracks and audio effects. When the player opens a case with a large amount of money, a sound with “good selection” meaning will be played. Otherwise, a sound with “bad selection” meaning will be played. There are other soundtracks added as well, please watch the video for details. 

Here is an image of the final graphic user interface:

![GUI](https://github.com/andrewljc0801/Interactive-Lab-Hub/blob/Spring2021/Final%20Project/Design/Deal%20Or%20No%20Deal%20UI.png?raw=true)

----------------------------------

### Prototype Design

In order to design the appearance of the Deal or No Deal game, we first need to decide what devices to use for the different features of the game.
* The positions of the case and the price board: Create an User Interface by using tkinter and a physical board with printed briefcases.
* Pick briefcases: Use two capacitive touch sensors to simulate the briefcase picking process in the real Deal or No Deal game. Each sensor connects to 12 briefcases.
* Briefcase’s cash value: Each case is opened as it is chosen, and the amount inside is removed from the price board on the interface. Different sound effects are played depending on the amount of cash value inside the briefcase.
* Banker’s Offer: Add the phone ringing sound effect.
* Deal or No Deal options: use the SparkFun Qwiic Red Button for the “No Deal” option and the SparkFun Qwiic Green Button for the “Deal” option.

Here are the front side and back side design of the device:

![Prototype_Front](https://github.com/andrewljc0801/Interactive-Lab-Hub/blob/Spring2021/Final%20Project/Design/Deal%20Or%20No%20Deal%20Prototype%20Front.jpg?raw=true)

![Prototype_Back](https://github.com/andrewljc0801/Interactive-Lab-Hub/blob/Spring2021/Final%20Project/Design/Deal%20Or%20No%20Deal%20Prototype%20Back.jpg?raw=true)

After gathering the devices needed to build the device, we designed a paper prototype that demonstrates how the parts should be connected. Instead of having 26 briefcases as shown in the original game, we removed two briefcases from the model because of the limited number of keys on the capacitive touch sensors. On the front side of the board, the briefcases and the “Deal” and “No Deal” buttons were placed based on the locations of items showing in the graphic user interface. It allows the player to track and select the cases easily. On the back side of the board, we drilled 24 holes, one for each briefcase. We placed two capacitive touch sensors on the left and right side of the board horizontally. By doing this, keys can be connected to the briefcases evenly and with the least amount of copper tape. The default I2C address for the Adafruit MPR121 12-Key Capacitive Touch Sensor is 0x5A. To make both capacitive touch sensors work, we bridged the jumper ADDR by using the soldering iron to change the I2C address on capacitive touch sensor B to 0x5B. Also, we changed the I2C address on the green button from default to 0x60 by closing the four solder jumpers on the board (labeled A0, A1, A2 and A3).

To complete the design, we added four legs on the four corners to support the board and to ensure the stability of the board.

Here are the images of the finished device:

![Front](https://github.com/andrewljc0801/Interactive-Lab-Hub/blob/Spring2021/Final%20Project/Design/Front.jpg?raw=true)

![Back](https://github.com/andrewljc0801/Interactive-Lab-Hub/blob/Spring2021/Final%20Project/Design/Back.jpg?raw=true)

![Whole_Device](https://github.com/andrewljc0801/Interactive-Lab-Hub/blob/Spring2021/Final%20Project/Design/Fully%20Connected%20Device.jpg?raw=true)

----------------------------------

### Final Video

[![Final_Video](https://github.com/andrewljc0801/Interactive-Lab-Hub/blob/Spring2021/Final%20Project/Design/Deal%20Or%20No%20Deal%20Background.jpg)](https://www.youtube.com/watch?v=wHek0vP4rhU)

----------------------------------

### Reflections

* Initially, we used the copper tape to bridge the jumper ADDR on the capacitive sensor board. However, it didn’t work well (sometimes the “bridge” was broken so the device was disconnected and fully undetectable). By searching the solutions online, we finally decided to buy a soldering iron to sturdily bridge the jumper. It took us a long time to figure out this solution, and it was close to the deadline when we bought the soldering iron. We wished we could research more about bridging the jumper before we start working on it.
* Another thing that we wish we knew sooner was “Check the functionality of the device after adding every new feature”. When we were testing our game, we encountered problems and realized that we had to remove some parts from the board to figure out what went wrong and to fix the problem. If we could check that our game works after a new feature was added, we could save a lot of time from finding out what the problem is. 
