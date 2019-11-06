from tkinter import *
from tkinter import messagebox
from random import randint
from time import sleep as wait


# Setup---

root = Tk()
root.title("Rock Paper Scissors")

# root.geometry("200x200")
selects = ("Rock", "Paper", "Scissors")



def AIselect():
    return selects[randint(0, 2)]

def showRules ():
    messagebox.showinfo("Rules.","Rock > Scissors\nPaper > Rock\nScissors > Paper\n\n"
                                 "If your choice is superior to the computer then you will gain a win\n"
                                 "However if your choice is inferior to what the computer chose you will gain a loss\n"
                                 "If you both pick the same choice then it will return a draw and neither side will"
                                 "win or lose")
def showHelp ():
    messagebox.showinfo("Help?","This is Rock Paper Scissors\nOn the Top there are 3 options, Rock, Paper and Scissors"
                                "Click these buttons to input your option, The Top Left will inform you on what you"
                                "have currently selected, Once you have selected, press submit at the bottom "
                                "to see what your opponent chose\nAlso at the top is your score board,This will inform "
                                "you of what how many Wins and Loses you have\n\nIn the Middle is the Output,This will"
                                "Inform you of what the Computer chose and if you have won or not.")


class Application():
    def __init__(self, master):
        # Variables---
        self.user_select = "NIL"
        self.ai_select = AIselect()
        self.locked_select = ""
        self.win = 0
        self.lose = 0
        self.logText = ""

        # Frames---
        self.optionFrame = Frame(root, bg="red")
        self.optionFrame.grid(row=0, column=1, sticky=N,columnspan=2)

        self.inputFrame = Frame(root, bg="red")
        self.inputFrame.grid(row=2, column=1,columnspan=2)

        self.outputFrame = Frame(root, bg="blue")
        self.outputFrame.grid(row=0, column=1, sticky=W)

        self.logFrame = Frame(root, bg="blue")
        self.logFrame.grid(row=1, column=1,columnspan=2)

        # InputFrame Setup---
        rockButton = Button(self.optionFrame, text="Rock", command=self.chooseRock)
        paperButton = Button(self.optionFrame, text="Paper", command=self.choosePaper)
        scissorsButton = Button(self.optionFrame, text="Scissors", command=self.chooseScissors)

        ruleButton = Button(self.inputFrame, text="Rules", command=showRules)
        submitButton = Button(self.inputFrame, text="Submit", command=self.submit)
        helpButton = Button(self.inputFrame, text="Help", command=showHelp)

        rockButton.grid(row=0, column=0)
        paperButton.grid(row=0, column=1)
        scissorsButton.grid(row=0, column=2)

        ruleButton.grid(row=0, column=1)
        submitButton.grid(row=0, column=0)
        helpButton.grid(row=0,column=2)

        # ScrollBar ?
        s = Scrollbar(self.logFrame, )
        s.pack(side=RIGHT, fill=Y)

        # OutputFrame Setup ---
        self.currentSelect = Label(self.outputFrame, text="Select", anchor=W,relief=FLAT)
        self.score = Label(self.outputFrame, text="Wins:" + str(self.win) + " Loses:" + str(self.lose), anchor=W,relief=RIDGE)
        self.log = Text(self.logFrame, )
        self.log.config(text="You have a connected")

        self.currentSelect.grid(row=0, column=0, sticky=W + N + S + E)
        self.score.grid(row=1, column=0, sticky=W + N + S + E)
        # self.log.grid(row=2, column=0, sticky=W + E)
        self.log.pack(side=LEFT)

        # Binding scrollbar to Log
        s.config(command=self.log.yview)
        self.log.config(yscrollcommand=s.set)

    def chooseRock(self):
        self.user_select = "Rock"
        self.updateCurrentSelect()

    def choosePaper(self):
        self.user_select = "Paper"
        self.updateCurrentSelect()

    def chooseScissors(self):
        self.user_select = "Scissors"
        self.updateCurrentSelect()

    def updateCurrentSelect(self):
        self.currentSelect.config(text=self.user_select)

    def updateScore(self):
        self.score.config(text="Wins : " + str(self.win) + "  Loses : " + str(self.lose))

    def submit(self):
        self.locked_select = self.user_select
        self.logic()

    def logic(self):

        # Logic
        # Rock > Scissors
        # Scissors > Paper
        # Paper > Rock

        ai = self.ai_select
        user = self.locked_select

        if ai == user:
            verdict = "Draw"
        elif user == "Rock" and ai == "Scissors":
            verdict = "Won"
        elif user == "Scissors" and ai == "Paper":
            verdict = "Won"
        elif user == "Paper" and ai == "Rock":
            verdict = "Won"
        else:
            verdict = "Lost"

        self.logText = str("You have chosen " + self.locked_select + " and the Computer chose " + \
                           self.ai_select + ". So you have " + verdict + "\n")
        self.log.insert(END, self.logText)

        if verdict == "Won":
            self.win = self.win + 1
        elif verdict == "Lost":
            self.lose = self.lose + 1

        self.updateScore()
        self.ai_select = AIselect()
        self.user_select = "NIL"
        self.currentSelect.config(text="Select")


Application(root)


root.mainloop()

wait(3)