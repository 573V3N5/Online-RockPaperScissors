import socket
from threading import *
import _thread
from tkinter import *
from tkinter import messagebox
from time import sleep

buff_size = 15
HEADER_SIZE = 10

Port = 6969
Host_IP = socket.gethostbyname(socket.gethostname())

ip = ''
playerName = ''

rpsOps = ("Rock","Paper","Scissors")

class server ():
    def __init__(self):
        self.p1Option = ''
        self.p2Option = ''
        self.p1name = ''
        self.p2name = ''
        #Connections
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((Host_IP,Port))
        self.server.listen()

        self.clients = []
        self.addr = []
        self.names = []

        #addC = Thread(target=self.add)  # Will make the process of Add a thread so it will always run in backround
        print(f"Waiting for 2 Players to join the server: {Host_IP}")
        self.add()
        print("2 players have joined")
        #addC.start()  # Starts the thread

        self.manageGame(self.clients,self.server)
    def add(self):
            global c
            n = 0
            while True:
                if n == 2:
                    break
                c, addr = self.server.accept()  # Accept any connection and save its address and "It" as C
                print(f"New Connection from {c.getpeername()}")  # New connection from (client name)
                self.clients.append(c)  # Will add the client to the clients array
                self.addr.append(addr)
                #clientInfo = c.recv(1024).decode()  # The client will send Info which i will print
                #print(f"The Client said \"{clientInfo}\"")  # Print clients info
                #c.send((f'You have succesfully connected to {socket.gethostbyname(socket.gethostname())}').encode())  # Send a message back to the client confirming their connection
                n += 1
    def manageGame (self,clients,server):
        print("Starting Game")
        p1 = clients[0]
        p2 = clients[1]

        name1 = Thread(target=self.getP1name,args=(p1,))
        name2 = Thread(target=self.getP2name, args=(p2,))
        name1.start()
        name2.start()
        name1.join()
        name2.join()

        name1 = self.p1name
        name2 = self.p2name

        print(f"Player One username is {self.p1name}\nPlayer Two username is {self.p2name}")

        self.clients[0].send(self.send(name2))
        self.clients[1].send(self.send(name1))


        while True:
            #Send Go Ahead
            #for conn in clients:
                #conn.sendall(self.sendGo())
            #print("SENT GO AHEAD")
            #Get Options
            getP1Choice = Thread(target=self.getP1,args=(p1,))
            getP2Choice = Thread(target=self.getP2, args=(p2,))
            getP1Choice.start()
            getP2Choice.start()
            print("Waiting for two options")
            getP1Choice.join()
            getP2Choice.join()
            print("Received two options")
            #SendOthersOptions to opponent
            p1Choice = self.send(self.p1Option)
            p2Choice = self.send(self.p2Option)
            self.clients[0].send(p2Choice)
            self.clients[1].send(p1Choice)

    def sendGo(self):  # Function for sending messages  #Dont think this is used anymore
        msg = "Go"
        msg = f'{len(msg):<{HEADER_SIZE}}' + msg  # Adds a header to the message containg the length of message
        return msg.encode()  # Returns the encoded message

    def send(self,x):  # Function for sending messages  # Message is Input
        msg = x
        msg = f'{len(msg):<{HEADER_SIZE}}' + msg  # Adds a header to the message containg the length of message
        return msg.encode()  # Returns the encoded message

    def getP1(self, x):
        while True:
            try:
                full_msg = ''
                isNew_msg = 1
                msglen = 0
                data = x.recv(buff_size)
                first_buff = 1
                isNew_msg = 1
                if data:
                    while True:
                        if first_buff == 1:
                            new_msg = data
                            first_buff = 0
                        else:
                            new_msg = x.recv(buff_size)
                        if isNew_msg == 1:
                            print("Received Message")
                            msglen = new_msg[:HEADER_SIZE]
                            isNew_msg = 0

                        full_msg += new_msg.decode()

                        if len(full_msg[HEADER_SIZE:]) == int(msglen):
                            full_msg = full_msg[HEADER_SIZE:]
                            print(full_msg)
                            self.p1Option = full_msg
                            break
                break
            except socket.error:
                self.p1Option = "error"
                errorMsg = self.send(self.p1Option)
                self.clients[1].send(errorMsg)

    def getP2 (self,x):
        while True:
            try:
                full_msg = ''
                isNew_msg = 1
                msglen = 0
                data = x.recv(buff_size)
                first_buff = 1
                isNew_msg = 1
                if data:
                    while True:
                        if first_buff == 1:
                            new_msg = data
                            first_buff = 0
                        else:
                            new_msg = x.recv(buff_size)
                        if isNew_msg == 1:
                            print("Received Message")
                            msglen = new_msg[:HEADER_SIZE]
                            isNew_msg = 0

                        full_msg += new_msg.decode()

                        if len(full_msg[HEADER_SIZE:]) == int(msglen):
                            full_msg = full_msg[HEADER_SIZE:]
                            print(full_msg)
                            self.p2Option = full_msg
                            break
                break
            except socket.error:
                self.p2Option = "error"
                errorMsg = self.send(self.p2Option)
                self.clients[0].send(errorMsg)


    def getP1name(self, x):
        while True:
            full_msg = ''
            isNew_msg = 1
            msglen = 0
            data = x.recv(buff_size)
            first_buff = 1
            isNew_msg = 1
            if data:
                while True:
                    if first_buff == 1:
                        new_msg = data
                        first_buff = 0
                    else:
                        new_msg = x.recv(buff_size)
                    if isNew_msg == 1:
                        print("Received Name")
                        msglen = new_msg[:HEADER_SIZE]
                        isNew_msg = 0

                    full_msg += new_msg.decode()

                    if len(full_msg[HEADER_SIZE:]) == int(msglen):
                        full_msg = full_msg[HEADER_SIZE:]
                        print(full_msg)
                        self.p1name = full_msg
                        break
            break

    def getP2name(self, x):
        while True:
            full_msg = ''
            isNew_msg = 1
            msglen = 0
            data = x.recv(buff_size)
            first_buff = 1
            isNew_msg = 1
            if data:
                while True:
                    if first_buff == 1:
                        new_msg = data
                        first_buff = 0
                    else:
                        new_msg = x.recv(buff_size)
                    if isNew_msg == 1:
                        print("Received Name")
                        msglen = new_msg[:HEADER_SIZE]
                        isNew_msg = 0

                    full_msg += new_msg.decode()

                    if len(full_msg[HEADER_SIZE:]) == int(msglen):
                        full_msg = full_msg[HEADER_SIZE:]
                        print(full_msg)
                        self.p2name = full_msg
                        break
            break


class client ():
    def __init__(self):
        #Connection Setup
        self.ip = ip
        self.name = playerName
        self.other = ''
        self.has = False
        self.kill = False

        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect((self.ip,Port))
        self.client.send(self.send2Serv(self.name))
        print("Waiting for another computer to connect")
        self.getOtherName(self.client)
        print(self.other)
        print(f"Connected to {self.ip}")


        self.root = Tk()
        self.root.title("Rock Paper Scissors Online")
        #Variables
        self.user_select = ''
        self.rival = ''
        self.lose = 0
        self.win = 0
        # Frames---
        self.optionFrame = Frame(self.root, bg="red")
        self.optionFrame.grid(row=0, column=1, sticky=N, columnspan=2)

        self.inputFrame = Frame(self.root, bg="red")
        self.inputFrame.grid(row=2, column=1, columnspan=2)

        self.outputFrame = Frame(self.root, bg="blue")
        self.outputFrame.grid(row=0, column=1, sticky=W)

        self.logFrame = Frame(self.root, bg="blue")
        self.logFrame.grid(row=1, column=1, columnspan=2)

        # InputFrame Setup---
        rockButton = Button(self.optionFrame, text="Rock", command=self.chooseRock)
        paperButton = Button(self.optionFrame, text="Paper", command=self.choosePaper)
        scissorsButton = Button(self.optionFrame, text="Scissors", command=self.chooseScissors)

        ruleButton = Button(self.inputFrame, text="Rules",)
        submitButton = Button(self.inputFrame, text="Submit", command = self.doGame)
        helpButton = Button(self.inputFrame, text="Help",)

        rockButton.grid(row=0, column=0)
        paperButton.grid(row=0, column=1)
        scissorsButton.grid(row=0, column=2)

        ruleButton.grid(row=0, column=1)
        submitButton.grid(row=0, column=0)
        helpButton.grid(row=0, column=2)

        # ScrollBar ?
        s = Scrollbar(self.logFrame, )
        s.pack(side=RIGHT, fill=Y)

        # OutputFrame Setup ---
        self.currentSelect = Label(self.outputFrame, text="Select", anchor=W, relief=FLAT)
        self.score = Label(self.outputFrame, text="Wins:" + str(self.win) + " Loses:" + str(self.lose), anchor=W,
                           relief=RIDGE)
        self.log = Text(self.logFrame, )

        self.currentSelect.grid(row=0, column=0, sticky=W + N + S + E)
        self.score.grid(row=1, column=0, sticky=W + N + S + E)
        # self.log.grid(row=2, column=0, sticky=W + E)
        self.log.pack(side=LEFT)

        # Binding scrollbar to Log
        s.config(command=self.log.yview)
        self.log.config(yscrollcommand=s.set)

        self.log.insert(END,f"You are connected to {self.ip}\nYour Opponent is : {self.other}")

        self.root.mainloop()
        input()
    def getIp (self):
        if self.nameIs.get() == "":
            self.name = "Player"
        else:
            self.name = self.nameIs.get()
        self.ip = self.ipIs.get()
        print(self.ip)
        print(self.name)
        self.firstTk.destroy()

    def getOtherName(self,x):
        while True:
            full_msg = ''
            isNew_msg = 1
            msglen = 0
            data = x.recv(buff_size)
            first_buff = 1
            isNew_msg = 1
            if data:
                while True:
                    if first_buff == 1:
                        new_msg = data
                        first_buff = "Received First Buffer"
                    else:
                        new_msg = x.recv(buff_size)
                    if isNew_msg == 1:
                        print("The server is sending a message")
                        msglen = new_msg[:HEADER_SIZE]
                        isNew_msg = 0

                    full_msg += new_msg.decode()
                    if len(full_msg[HEADER_SIZE:]) == int(msglen):
                        full_msg = full_msg[HEADER_SIZE:]
                        self.other = full_msg
                        break  # Break and restart
                break


    def chooseRock(self):
        self.user_select = rpsOps[0]
        self.updateCurrentSelect()

    def choosePaper(self):
        self.user_select =  rpsOps[1]
        self.updateCurrentSelect()

    def chooseScissors(self):
        self.user_select = rpsOps[2]
        self.updateCurrentSelect()

    def updateCurrentSelect(self):
        self.currentSelect.config(text=self.user_select)

    def updateScore(self):
        self.score.config(text="Wins : " + str(self.win) + "  Loses : " + str(self.lose))

    def send2Serv(self,x):
        msg = x
        msg = f'{len(msg):<{HEADER_SIZE}}' + msg
        return msg.encode()

    def logic (self,rival):
        us = self.user_locked
        them = rival
        print(them)

        if them == us:
            verdict = "Draw"
        elif us == rpsOps[0] and them == rpsOps[2]:
            verdict = "Won"
        elif us == rpsOps[2] and them == rpsOps[1]:
            verdict = "Won"
        elif us == rpsOps[1] and them == rpsOps[0]:
            verdict = "Won"
        else:
            verdict = "Lost"

        if verdict == "Won":
            self.win += 1
        elif verdict == "Lost":
            self.lose += 1

        self.updateScore()
        self.user_select = "NIL"
        self.log.insert(END,f"\n{self.other} chose {rival}\nYou {verdict}")
        self.currentSelect.config(text="Select")
        print("Finished Logic")

    def errorTime (self):
        self.log.insert(END,f"The server has ran into an error\nClosing Program in 10 seconds")
        sleep(10)
        self.client.close()
        self.root.quit()


    def doGame (self):
        self.user_locked = self.user_select
        self.log.insert(END,f"\nYou chose {self.user_locked}")
        sendIt = self.send2Serv(self.user_locked)
        self.client.send(sendIt)

        full_msg = ''
        isNew_msg = 1
        msglen = 0
        data = self.client.recv(buff_size)  # All these variables are self explanatory
        first_buff = 1
        isNew_msg = 1
        rival = 69
        var1  =1
        while var1 == 1:
            if data:
                print("Received Data")
                while True:
                    if first_buff == 1:  # Checks to see if its on its first buffer and if it is use the first buffer
                        new_msg = data
                        first_buff = "not 0"
                    else:  # If its in the middle , use the new recived buffer
                        new_msg = self.client.recv(buff_size)
                    if isNew_msg == 1:
                        print("The server is sending a message")
                        msglen = new_msg[:HEADER_SIZE]  # Message Length is whatever length is stored in the Header
                        isNew_msg = 0

                    full_msg += new_msg.decode()  # Full message is before + new buffer

                    if len(full_msg[HEADER_SIZE:]) == int(msglen):  # If the full message is now equal to message length
                        full_msg = full_msg[HEADER_SIZE:]  # Full message is everything after the header
                        print(full_msg)
                        rival = full_msg
                        var1 = 0
                        break
        if rival != "error":
            self.logic(rival)
            print("Finished doGame")
        elif rival == "error":
            print("Server sent error")
            self.errorTime()


def getIp(nameIs,ipIs,firstTk):
            global ip
            global playerName
            if nameIs.get() == "":
                name = "Player"
            else:
                name = nameIs.get()
            ip = ipIs.get()
            playerName = name
            firstTk.destroy()

def helpBox ():
    messagebox.showinfo("Help!", "Lol havnt had this yet LMAO")

def start ():
        ip = ''
        name = ''
        other = ''
        has = False
        print( f"Your IP is {socket.gethostbyname(socket.gethostname())}")
        firstTk = Tk()
        firstTk.title("Connect To Server")
        ipPrompt = Label(firstTk,text="Server IP",anchor=E)
        ipPrompt.grid(row=0,column=0)
        ipSubmit = Button(firstTk,text="Submit",command = lambda: getIp(nameIs,ipIs,firstTk),anchor=E)
        ipSubmit.grid(row=1,column=3)
        help = Button(firstTk,text="Help",command =helpBox,anchor=E)
        help.grid(row=1,column=4)
        ipIs = Entry(firstTk)
        ipIs.grid(row=0,column=2)

        namePrompt = Label(firstTk,text="Name",anchor=E)
        namePrompt.grid(row=1,column=0,sticky=E)
        nameIs = Entry(firstTk)
        nameIs.grid(row=1,column=2,sticky=E)
        #namePrompt =
        print("...WAITING FOR IP")
        firstTk.mainloop()

start()
print("left start")
if ip == "server":
    print("Selected Server")
    server = server()
else:
    client = client()

input()
