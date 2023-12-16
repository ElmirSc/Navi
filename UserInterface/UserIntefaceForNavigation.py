import tkinter as tk
from PIL import Image,ImageTk, ImageDraw
import cv2
import numpy as np
from .UserInterfaceConfig import *
from .StreetSign import *

class userInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.tk = tk
        self.instruction = instructionStartPoint
        self.tkinterSpeed = 0
        self.tkinterCurrentDrivenDistance = 0
        self.streetSign = streetSign()
        self.entry = None
        self.startPoint = 0
        self.endPoint = 0
        self.userInputIsReady = False
        self.tkinterInstruction = 0
        self.speed = 0
        self.dist = 0
        self.tkinterImage = 0
        self.endedProgramm = False
        self.button = 0

    def initUI(self):
        print("init Gui started")
        # Setze die Fenstergröße auf 800x600 Pixel
        self.root.geometry("1000x530")
        self.root.maxsize(800, 700)
        # Ändern Sie die Hintergrundfarbe auf hellgrün
        self.root.configure(bg="#45BD6A")
        self.root.title("Navigation")

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=1)
        self.root.columnconfigure(4, weight=1)

        # root.rowconfigure(0,weight=2)
        self.root.rowconfigure(0, weight=5)
        self.root.rowconfigure(1, weight=2)

        #Zellen einstellen
        for i in range(2):
            for j in range(5):
                if i != 0:
                    # frame = tk.Frame(root, borderwidth=1, relief="solid", width=160, height=50,bg="lightgreen")
                    frame = self.tk.Frame(self.root, width=200, height=50, bg="lightgreen")
                    frame.grid(row=i, column=j)
                else:
                    if j == 0 and i == 0:
                        # frame = tk.Frame(root, borderwidth=1, relief="solid", width=800, height=500,bg="lightgreen")
                        frame = self.tk.Frame(self.root, width=1000, height=500, bg="lightgreen")
                        frame.grid(row=i, column=j, columnspan=5)

        image = Image.open("../UserInterface/street.png")
        resizedImage = image.resize((800, 500))
        imageTk = ImageTk.PhotoImage(resizedImage)
        self.tkinterImage = self.tk.Label(self.root, image=imageTk, bg="lightgreen")
        self.tkinterImage.grid(row=0, column=0, columnspan=5, sticky="")

        self.tkinterInstruction = self.tk.Label(self.root, text=str(self.instruction), bg="lightgreen", foreground="black", width=30, height=1)
        self.tkinterInstruction.grid(row=1, column=0, sticky="w")

        self.button = self.tk.Button(self.root, text="Start",command=self.startButtonPressed)
        self.button.grid(row=1, column=1, sticky="")

        entry = self.tk.Entry(self.root)
        self.entry = entry
        #entry.pack()
        # Füge Event-Binding für die Enter-Taste hinzu
        entry.bind("<Return>", self.get_input)
        # Setze den Fokus auf das Entry-Widget, damit die Enter-Taste funktioniert
        entry.focus_set()
        entry.grid(row=1, column=2, sticky="")


        self.tkinterSpeed = self.tk.Label(self.root, text="Speed: " + str(self.speed) + " (km/h)", foreground="black", bg="lightgreen", width=20, height=1)
        self.tkinterSpeed.grid(row=1, column=3, sticky="")

        self.tkinterCurrentDrivenDistance = self.tk.Label(self.root, text="Distance: " + str(self.dist) + " m", foreground="black", bg="lightgreen")
        self.tkinterCurrentDrivenDistance.grid(row=1, column=4, sticky="")

        # Definiere die Funktion, die ausgeführt wird, wenn das Fenster geschlossen wird
        self.root.protocol("WM_DELETE_WINDOW", self.setClosedProgramm)

        self.root.mainloop()

    def setClosedProgramm(self):
        self.endedProgramm = True
        self.root.destroy()

    def getClosedProgramBool(self):
        return self.endedProgramm

    def drawRouteInMap(self,routeCcoords):
        print("drawRoute")
        img = cv2.imread("../UserInterface/street.PNG", cv2.COLOR_BGR2GRAY)
        nodeCoordsInMap = np.loadtxt("../UserInterface/nodeCordOnMap.txt").astype(int)
        for i in range(len(routeCcoords)):
            if i + 1 < len(routeCcoords):
                first = routeCcoords[i] - 1
                next = routeCcoords[i + 1] - 1
                cv2.line(img, (nodeCoordsInMap[first][0], nodeCoordsInMap[first][1]),
                         (nodeCoordsInMap[next][0], nodeCoordsInMap[next][1]), (0, 0, 255), 1)
        #cv2.imshow("test", img)
        cv2.imwrite("../UserInterface/map_with_route.png", img)
        # Bild in das Tkinter Label laden und aktualisieren
        updated_image = Image.open("../UserInterface/map_with_route.png")
        resized_image = updated_image.resize((800, 500))
        imageTk = ImageTk.PhotoImage(resized_image)
        self.tkinterImage.config(image=imageTk)
        self.tkinterImage.image = imageTk

    def updateUiToStartAgain(self):
        self.button.config(text="Start", command=self.startButtonPressed)
        image = Image.open("../UserInterface/street.png")
        resizedImage = image.resize((800, 500))
        imageTk = ImageTk.PhotoImage(resizedImage)
        self.tkinterImage.config(image=imageTk)
        self.tkinterImage.image = imageTk
        self.instruction = instructionStartPoint
        self.updateInstructionInGUI()
        self.userInputIsReady = False
        self.setDistance(0)
        return

    def get_input(self,event):
        userInput = self.entry.get()  # Hole die Eingabe aus dem Entry-Widget
        print(userInput)
        if self.instruction == instructionStartPoint:
            self.instruction = instructionEndPoint
            self.startPoint = self.getDrivingPointFromInputAndConvertItToANumber(userInput)
        elif self.instruction == instructionEndPoint:
            self.endPoint = self.getDrivingPointFromInputAndConvertItToANumber(userInput)
            self.instruction = instructionWaitForStartButton
        else:
            print("Benutzereingabe passt nicht:", userInput)
        self.updateInstructionInGUI()
        self.entry.delete(0,self.tk.END)

    def getIfUserInputIsReady(self):
        return self.userInputIsReady

    def getStartPointForNavigation(self):
        return int(self.startPoint)

    def getEndPointForNavigation(self):
        return int(self.endPoint)

    def setDistance(self,cost):
        self.dist = int(cost)
        self.updateDrivenDistance(self.dist)

    def updateInstructionInGUI(self):
        self.tkinterInstruction.config(text = self.instruction)

    def updateSpeed(self,currentSpeed):
        self.speed = currentSpeed
        self.tkinterSpeed.config(text="Speed: " + str(currentSpeed) + " (km/h)")

    def updateDrivenDistance(self,dist):
        #self.dist = dist
        self.tkinterCurrentDrivenDistance.config(text="Distance: " + str(dist) + " m")

    def updateButton(self):
        if self.instruction == instructionDrive:
            self.button.config(text="End",command=self.endButtonPressed)
        elif self.instruction == instructionEndDriving:
            self.updateUiToStartAgain()


    def startButtonPressed(self):
        self.userInputIsReady = True
        self.instruction = instructionDrive
        self.updateInstructionInGUI()
        self.updateButton()

    def endButtonPressed(self):
        #self.userInputIsReady = True
        self.instruction = instructionEndDriving
        self.updateInstructionInGUI()
        self.updateButton()

    def getDrivingPointFromInputAndConvertItToANumber(self, input):
        numb = 0
        match input.lower():
            case "a":
                numb = 1
            case "b":
                numb = 2
            case "c":
                numb = 3
            case "d":
                numb = 4
            case "e":
                numb = 5
            case "f":
                numb = 6
            case "g":
                numb = 7
            case "h":
                numb = 8
            case "i":
                numb = 9
            case "j":
                numb = 10
            case "k":
                numb = 11
            case "l":
                numb = 12
        return numb


if __name__ == "__main__":
    ui = userInterface()
    ui.initUI()
    #while(True):
    #    ui.drawRouteInMap(1,2)