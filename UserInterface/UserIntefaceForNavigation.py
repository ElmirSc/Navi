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

        image = Image.open("UserInterface/street_with_node_nummeration.png")
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

    def position_car_on_map(self,standing_of_car_on_map):
        car = cv2.imread("UserInterface/car2.png",cv2.IMREAD_UNCHANGED)
        car_resized = cv2.resize(car,(10, 20))
        car_resized = self.get_rotated_car(standing_of_car_on_map, car_resized)

        map = cv2.imread("UserInterface/map_with_route.png", cv2.IMREAD_UNCHANGED)
        # Erstelle einen leeren Alphakanal mit denselben Dimensionen wie das Bild
        height, width = map.shape[:2]
        alpha_channel = np.ones((height, width),
                                dtype=np.uint8) * 255  # Fülle den Alphakanal mit voller Transparenz (255)

        # Füge den Alphakanal dem Bild hinzu
        map = cv2.merge((map, alpha_channel))

        nodeCoordsInMap = self.loadNodeCoords()

        car_height, car_width = car_resized.shape[:2]

        x_position = nodeCoordsInMap[self.startPoint-1][0] - int(car_width/2)
        y_position = nodeCoordsInMap[self.startPoint-1][1] - int(car_height/2)

        # Platzieren des Auto-Bildes auf dem Hauptbild an den angegebenen Koordinaten
        map[y_position:y_position + car_height, x_position:x_position + car_width] = car_resized

        # Speichern des resultierenden Bildes mit dem platzierten Auto
        cv2.imwrite("UserInterface/map_with_route.png", map)
        updated_image = Image.open("UserInterface/map_with_route.png")
        resized_image = updated_image.resize((800, 500))
        imageTk = ImageTk.PhotoImage(resized_image)
        self.tkinterImage.config(image=imageTk)
        self.tkinterImage.image = imageTk

    def update_position_of_car_on_map(self,current_node, next_node, standing_of_car_on_map,current_cost, cost_between_nodes):
        car = cv2.imread("UserInterface/car2.png", cv2.IMREAD_UNCHANGED)
        car_resized = cv2.resize(car, (10, 20))
        car_resized = self.get_rotated_car(standing_of_car_on_map, car_resized)

        pixels_between_two_nodes_x = 0
        pixels_between_two_nodes_y = 0
        pixel_of_one_cost = 0
        current_pixel_cost_on_map = 0
        y_position = 0
        x_position = 0

        if current_node[0] == next_node[0]:
            pixels_between_two_nodes_y = current_node[1] - next_node[1]
            x_position = current_node[0]
            pixel_of_one_cost = pixels_between_two_nodes_y / cost_between_nodes
            current_pixel_cost_on_map = pixel_of_one_cost * current_cost
            y_position = y_position + current_pixel_cost_on_map

        if current_node[1] == next_node[1]:
            pixels_between_two_nodes_x = current_node[0] - next_node[0]
            y_position = current_node[1]
            pixel_of_one_cost = pixels_between_two_nodes_x / cost_between_nodes
            current_pixel_cost_on_map = pixel_of_one_cost * current_cost
            x_position = x_position + current_pixel_cost_on_map

        map = cv2.imread("UserInterface/map_with_route.png", cv2.IMREAD_UNCHANGED)
        # Erstelle einen leeren Alphakanal mit denselben Dimensionen wie das Bild
        height, width = map.shape[:2]
        alpha_channel = np.ones((height, width),
                                dtype=np.uint8) * 255  # Fülle den Alphakanal mit voller Transparenz (255)

        # Füge den Alphakanal dem Bild hinzu
        map = cv2.merge((map, alpha_channel))

        car_height, car_width = car_resized.shape[:2]

        # Platzieren des Auto-Bildes auf dem Hauptbild an den angegebenen Koordinaten
        map[y_position:y_position + car_height, x_position:x_position + car_width] = car_resized

        # Speichern des resultierenden Bildes mit dem platzierten Auto
        cv2.imwrite("UserInterface/map_with_route.png", map)

        updated_image = Image.open("UserInterface/map_with_route.png")
        resized_image = updated_image.resize((800, 500))
        imageTk = ImageTk.PhotoImage(resized_image)
        self.tkinterImage.config(image=imageTk)
        self.tkinterImage.image = imageTk

    def get_rotated_car(self,standing_of_car_on_map,car_resized):
        match standing_of_car_on_map:
            case 1:
                car_resized = cv2.rotate(car_resized, cv2.ROTATE_90_COUNTERCLOCKWISE)
            case 2:
                car_resized = cv2.rotate(car_resized, cv2.ROTATE_90_CLOCKWISE)
            case 3:
                car_resized = cv2.rotate(car_resized, cv2.ROTATE_180)

        return car_resized
    def loadNodeCoords(self):
        return np.loadtxt("UserInterface/nodeCordOnMap.txt").astype(int)

    def drawRouteInMap(self,routeCcoords):
        print("drawRoute")
        img = cv2.imread("UserInterface/street_with_node_nummeration.png", cv2.COLOR_BGR2GRAY)
        nodeCoordsInMap = self.loadNodeCoords()
        for i in range(len(routeCcoords)):
            if i + 1 < len(routeCcoords):
                first = routeCcoords[i] - 1
                next = routeCcoords[i + 1] - 1
                cv2.line(img, (nodeCoordsInMap[first][0], nodeCoordsInMap[first][1]),
                         (nodeCoordsInMap[next][0], nodeCoordsInMap[next][1]), (0, 0, 255), 1)
        #cv2.imshow("test", img)
        cv2.imwrite("UserInterface/map_with_route.png", img)
        # Bild in das Tkinter Label laden und aktualisieren
        updated_image = Image.open("UserInterface/map_with_route.png")
        resized_image = updated_image.resize((800, 500))
        imageTk = ImageTk.PhotoImage(resized_image)
        self.tkinterImage.config(image=imageTk)
        self.tkinterImage.image = imageTk

    def updateUiToStartAgain(self):
        self.button.config(text="Start", command=self.startButtonPressed)
        image = Image.open("UserInterface/street_with_node_nummeration.png")
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

    def getDrivingInstructionsFromRoute(self,route):
        drivingInstructions = []
        nodeCoordsInMap = self.loadNodeCoords()
        current = 0
        prev = 0
        next = 0
        for i in range(0,len(route)):
            if i + 1 < len(route):
                if i == 0:
                    prev = route[i] - 1
                else:
                    prev = current
                current = route[i] - 1
                next = route[i + 1] - 1
                drivingInstructions.append(self.calcInstruction(nodeCoordsInMap[prev],nodeCoordsInMap[current], nodeCoordsInMap[next]))
        return drivingInstructions

    def calcInstruction(self,prev,cur,next):
        vertical = False
        horizontal = False

        if cur[0] == next[0] == prev[0] or cur[1] == next[1] == prev[1]:
            return "g"

        if prev[0] == cur[0]:
            vertical = True
        elif prev[1] == cur[1]:
            horizontal = True

        if vertical:
            if next[0] < cur[0] and cur[1] < prev[1] or next[0] > cur[0] and cur[1] > prev[1]:
                return "l"
            elif next[0] < cur[0] and cur[1] > prev[1] or next[0] > cur[0] and cur[1] < prev[1]:
                return "r"
        elif horizontal:
            if next[1] < cur[1] and cur[0] > prev[0] or next[1] > cur[1] and cur[0] < prev[0]:
                return "l"
            elif next[1] > cur[1] and cur[0] > prev[0] or next[1] < cur[1] and cur[0] < prev[0]:
                return "r"

        return 0

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