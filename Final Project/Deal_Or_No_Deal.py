# IDD Final Project - Deal Or No Deal
# Author: Andrew Liu and Quinn Wu (developed Harmehar Singh's project, Github link: https://github.com/SinghHarmehar/Deal-No-Deal)
# This game can be played by using Raspberry Pi, Qwiic button, and capacitive sensor. Speaker is needed.

import random
from playsound import playsound
from tkinter import Tk, Frame, Label, PhotoImage, Button
from tkinter import messagebox
from tkinter import *
import time
import os
import board
import busio
import adafruit_mpr121
import qwiic_button

# Money Value  
unshuffledListValues= [0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 500, 750, 1000, 5000, 25000, 50000, 75000, 100000, 200000, 300000, 400000, 500000, 750000, 1000000]      
# Gets a photo from the list imgBriefcases and returns said image
def increaseX(n):
    photo= imgBriefcases[n]
    return photo
# Close the game with options
def closeOption():
    answer = messagebox.askyesno("EXIT", "Are you sure you want to exit?")
    if answer == True:
        messagebox.showinfo("", "Thank you for playing Deal or No Deal!")
        exit()
# Create frames
def createFrames():
    global westframe, eastframe, centerframe, lastrowframe
    westframe = Frame(frame, padx=10, pady=10, bg="black")
    eastframe = Frame(frame, padx=10, pady=10, bg="black")
    centerframe = Frame(frame, padx=10, pady=10, bg="black", width=380, height=280)
    lastrowframe= Frame(centerframe, bg="black")

    westframe.grid(row=1, column=0)
    eastframe.grid(row=1, column=2)
    centerframe.grid(row=1, column=1)
    lastrowframe.grid(row=5, column=0, columns=6)
# Create buttons
def createButtons():
    global briefcaseList
    briefcaseList= [[] for cols in range(5)]
    briefcaseList[0]= [0] * 5
    briefcaseList[1]= [0] * 5
    briefcaseList[2]= [0] * 5
    briefcaseList[3]= [0] * 5
    x= 0
    while x < 20:
        for rows in range(len(briefcaseList)):
            for cols in range(len(briefcaseList[rows])):
                photo= increaseX(x)
                briefcaseList[rows][cols]= Button(centerframe, bg="black", bd=0, image= photo, command=lambda r=rows, c=cols: evaluateBriefcases(r, c))
                briefcaseList[rows][cols].grid(row=rows+1, column=cols, padx=7, pady=7, sticky="e")      
                x += 1        
    briefcaseList[4]= [0] * 4
    while x > 19 and x < 24:
        for cols in range(len(briefcaseList[4])):
            photo= increaseX(x)
            briefcaseList[rows][cols]= Button(lastrowframe, bg="black", bd=0, image= photo, command=lambda r=rows, c=cols: evaluateBriefcases(r, c))
            briefcaseList[rows][cols].grid(row=rows+1, column=cols, padx=7, pady=7, sticky="e")
            x += 1
            
def showSideLabels():

    r1= 0
    r2= 0
    for i, x in enumerate(labelList):
        if i < 12:
            if x == True:
                y= Label(westframe, image= imgCashLetter[i], background="black")
            else:
                y= Label(westframe,  background="black", image= imgBlankLabel)
            y.grid(row=r1, column=0, pady=3)
            r1 += 1
        else:
            if x == True:
                y= Label(eastframe, image= imgCashLetter[i], background="black")
            else:
                y= Label(eastframe, background="black", image= imgBlankLabel)
            y.grid(row=r2, column=0, pady=3)
            r2 += 1

def getBriefcaseVal(r, c):
    global boxNumber
    if r == 5:
        index= 20 + c
        boxNumber= index + 1
        a= listValues[index]    
    else:
        index= c + r * 5
        boxNumber= index + 1
        a= listValues[index]
    return a
 
def removeLabel(r, c):
    briefcaseVal= getBriefcaseVal(r, c)
    index= unshuffledListValues.index(briefcaseVal)
    labelList[index]= False
    showSideLabels()
    
def askPlayAgain():
    answer= messagebox.askyesno("Exit", "Do you want to play again?")        
    if answer == True:
        defaultSettings()
    elif answer == False:
        messagebox.showinfo("", "Thank you for playing Deal or No Deal!")
        exit()
        
# Bank offers    
def offerMoney():
    global totalMoney, counter, roundNum, briefcasesLeft, chosenBriefcaseVal, moneyVal, lblMessage
    # Bank's offer is calculated by dividing totalMoney by the amount of boxes left multiplied by roundNum divided by 10
    offer= (totalMoney / (24 - counter)) * roundNum / 10
    offer= "{:,.2f}".format(offer)
    playsound('sounds/bank_calling.mp3')
    lblMessage.config(text="The banker's offer is $" + str(offer) + "\nWould you like to take the deal?")
    root.update()
    answer = None
    while True:
        if green_button.is_button_pressed() == True:
            playsound('sounds/deal.mp3')
            print("Green button pressed.")
            answer = True
            break
        if red_button.is_button_pressed() == True:
            playsound('sounds/no_deal.mp3')
            print("Red button pressed.")
            answer = False
            break
    if answer == True:
        chosenBriefcaseVal= "{:,.2f}".format(chosenBriefcaseVal)
        messagebox.showinfo("", "Congrats...you are going home with $" + offer)
        messagebox.showinfo("", "The briefcase you selected has $" + chosenBriefcaseVal)
        askPlayAgain()
    elif answer == False:
        roundNum += 1
        
        if roundNum == 2:
            briefcasesLeft= 5
        elif roundNum == 3:
            briefcasesLeft= 4
        elif roundNum == 4:
            briefcasesLeft= 3
        elif roundNum == 5:
            briefcasesLeft= 2
        else:
            briefcasesLeft= 1            
        lblMessage.config(text="Choose " + str(briefcasesLeft) + " briefcase(s) to remove")
        counter += 1  
    
    if counter == 23:

        lastBriefcaseVal= totalMoney - chosenBriefcaseVal
        lastBriefcaseVal= "{:,.2f}".format(lastBriefcaseVal)
        lblMessage.config(text="There is only one case left!\nWould you like to keep your case?")
        root.update()
        answer2 = None
        while True:
            if green_button.is_button_pressed() == True:
                print("Green button pressed.")
                answer2 = True
                break
            if red_button.is_button_pressed() == True:
                print("Red button pressed.")
                answer2 = False
                break

        # User chooses to keep their case
        if answer2 == True:
            chosenBriefcaseVal= "{:,.2f}".format(chosenBriefcaseVal)
            messagebox.showinfo("", "Congrats...you're going home with $" + chosenBriefcaseVal)
        # User chooses to go with the other case
        elif answer2 == False:
            messagebox.showinfo("", "Congrats...you're going home with $" + lastBriefcaseVal)
        askPlayAgain()
           
def evaluateBriefcases(r, c):
    global counter, totalMoney, briefcasesLeft, chosenBriefcaseVal, moneyVal, lblMessage, lblPlayersCase, boxNumber
    if counter == 0:
        print(r,c)
        chosenBriefcaseVal= getBriefcaseVal(r, c)
        chosenBriefcase= briefcaseList[r][c].cget("image")
        briefcaseList[r][c].config(state="disabled", image=imgBlank)
        lblPlayersCase.config(image=chosenBriefcase)
        lblMessage.config(text="Choose " + str(briefcasesLeft) + " briefcase(s) to remove")
        counter += 1 
    elif counter >= 1:
        briefcasesLeft -= 1
        moneyVal= getBriefcaseVal(r, c)
        removeLabel(r, c)
        lblMessage.config(text="Briefcase #" + str(boxNumber) + " contains $" + "{:,.2f}".format(moneyVal))
        root.update()
        if moneyVal > 25000:
            playsound('sounds/bad_open.mp3')
        else:
            playsound('sounds/good_open.mp3')
        time.sleep(2)
        totalMoney= totalMoney - moneyVal
        briefcaseList[r][c].config(state="disabled", image=imgBlank)
        if counter in [6, 11, 15, 18, 20, 21, 22]:
            lblMessage.config(text="Choose " + str(briefcasesLeft) + " briefcase(s) to remove")
            offerMoney()
        elif counter not in [0, 6, 11, 15, 18, 20, 21, 22]:
            lblMessage.config(text="Choose " + str(briefcasesLeft) + " briefcase(s) to remove")
            counter += 1

            
def defaultSettings():
    global counter, totalMoney, roundNum, briefcasesLeft, chosenBriefcaseVal, moneyVal, labelList, listValues, lblMessage, lblPlayersCase
    labelList= [True] * 24
    counter= 0
    totalMoney= 3408016.01
    roundNum= 1
    briefcasesLeft= 6
    chosenBriefcaseVal= 0
    moneyVal= 0
    listValues= [0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 500, 750, 1000, 5000, 25000, 50000, 75000, 100000, 200000, 300000, 400000, 500000, 750000, 1000000]  
    random.shuffle(listValues)
    lblTitle = Label(frame, image=imgTitle, border=0)
    lblTitle.grid(row=0, column=0, columns=3)
    lblMessage = Label(frame, width=35, bg="black", font=("Century Gothic", 14, "bold"), fg="#fcea97", text="Choose one of the briefcases!", justify="center")   
    lblMessage.grid(row=2, column=1, padx=10, pady=5)
    lblPlayersCase = Label(frame, image=imgBlank, bg="black")
    lblPlayersCase.grid(row=2, column=0)
    createFrames()
    createButtons()
    showSideLabels()



i2c = busio.I2C(board.SCL, board.SDA)

mprA = adafruit_mpr121.MPR121(i2c, address=0x5a)
mprB = adafruit_mpr121.MPR121(i2c, address=0x5b)

red_button = qwiic_button.QwiicButton(0x6f)
green_button = qwiic_button.QwiicButton(0x60)
red_button.begin()
green_button.begin()

red_button.LED_off()
green_button.LED_off()

if not red_button.begin():
    print("Red Button is not connected.")
if not green_button.begin():
    print("Green Button is not connected.")


root = Tk()
root.title("Deal or No Deal")
root.protocol("WM_DELETE_WINDOW", closeOption)
frame = Frame(root, padx=10, pady=10, bg="black")
frame.pack()
imgTitle = PhotoImage(file="images/dond_logo.png")
imgBriefcases= [PhotoImage(file="images/suitcases/case1.png"), PhotoImage(file="images/suitcases/case2.png"), PhotoImage(file="images/suitcases/case3.png"),
                PhotoImage(file="images/suitcases/case4.png"), PhotoImage(file="images/suitcases/case5.png"), PhotoImage(file="images/suitcases/case6.png"),
                PhotoImage(file="images/suitcases/case7.png"), PhotoImage(file="images/suitcases/case8.png"), PhotoImage(file="images/suitcases/case9.png"),
                PhotoImage(file="images/suitcases/case10.png"), PhotoImage(file="images/suitcases/case11.png"), PhotoImage(file="images/suitcases/case12.png"),
                PhotoImage(file="images/suitcases/case13.png"), PhotoImage(file="images/suitcases/case14.png"), PhotoImage(file="images/suitcases/case15.png"),
                PhotoImage(file="images/suitcases/case16.png"), PhotoImage(file="images/suitcases/case17.png"), PhotoImage(file="images/suitcases/case18.png"),
                PhotoImage(file="images/suitcases/case19.png"), PhotoImage(file="images/suitcases/case20.png"), PhotoImage(file="images/suitcases/case21.png"),
                PhotoImage(file="images/suitcases/case22.png"), PhotoImage(file="images/suitcases/case23.png"), PhotoImage(file="images/suitcases/case24.png")]
#Here I created a list of PhotoImages that contain all 26 money labels and assigned said list to the imgCashLetter variable
imgCashLetter= [PhotoImage(file="images/money/0.01.png"), PhotoImage(file="images/money/1.png"), PhotoImage(file="images/money/5.png"), PhotoImage(file="images/money/10.png"), PhotoImage(file="images/money/25.png"),
                PhotoImage(file="images/money/50.png"), PhotoImage(file="images/money/75.png"), PhotoImage(file="images/money/100.png"), PhotoImage(file="images/money/200.png"), PhotoImage(file="images/money/300.png"), 
                PhotoImage(file="images/money/500.png"), PhotoImage(file="images/money/750.png"), PhotoImage(file="images/money/1000.png"), PhotoImage(file="images/money/5000.png"), 
                PhotoImage(file="images/money/10000.png"), PhotoImage(file="images/money/25000.png"), PhotoImage(file="images/money/50000.png"), PhotoImage(file="images/money/75000.png"),
                PhotoImage(file="images/money/200000.png"), PhotoImage(file="images/money/300000.png"), PhotoImage(file="images/money/400000.png"), PhotoImage(file="images/money/500000.png"), PhotoImage(file="images/money/750000.png"), 
                PhotoImage(file="images/money/1000000.png")] 
imgBlank= PhotoImage(file= "images/suitcases/blankcase.png")
imgBlankLabel= PhotoImage(file="images/money/blankmoney.png")

cap_sensor_to_case_number = {
    "A0": 3,
    "A1": 2,
    "A2": 1,
    "A3": 8,
    "A4": 7,
    "A5": 6,
    "A6": 11,
    "A7": 12,
    "A8": 17,
    "A9": 16,
    "A10": 22,
    "A11": 21,
    "B0": 14,
    "B1": 13,
    "B2": 10,
    "B3": 9,
    "B4": 5,
    "B5": 4,
    "B6": 23,
    "B7": 24,
    "B8": 18,
    "B9": 19,
    "B10": 20,
    "B11": 15
}

case_number_to_rc = {
    1: (0, 0),
    2: (0, 1),
    3: (0, 2),
    4: (0, 3),
    5: (0, 4),
    6: (1, 0),
    7: (1, 1),
    8: (1, 2),
    9: (1, 3),
    10: (1, 4),
    11: (2, 0),
    12: (2, 1),
    13: (2, 2),
    14: (2, 3),
    15: (2, 4),
    16: (3, 0),
    17: (3, 1),
    18: (3, 2),
    19: (3, 3),
    20: (3, 4),
    21: (4, 0),
    22: (4, 1),
    23: (4, 2),
    24: (4, 3)
}


defaultSettings()
while True:
    green_button.LED_on(200)
    red_button.LED_on(200)
    for i in range(12):
        if mprA[i].value:
            print(f"A {i} touched!")
            boxNumber = cap_sensor_to_case_number["A"+str(i)]
            r, c = case_number_to_rc[boxNumber]
            evaluateBriefcases(r, c)
        if mprB[i].value:
            print(f"B {i} touched!")
            boxNumber = cap_sensor_to_case_number["B"+str(i)]
            r, c = case_number_to_rc[boxNumber]
            evaluateBriefcases(r, c)
    time.sleep(0.4)  # Small delay    
    root.update()
