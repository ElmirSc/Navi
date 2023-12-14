import tkinter as tk
from PIL import Image,ImageTk, ImageDraw
import cv2
import numpy as np
from UserInterfaceConfig import *
from StreetSign import *

class userInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.tk = tk
        self.instruction = instructionStartPoint
        self.speed = 10
        self.dist = 10
        self.streetSign = streetSign()
        self.entry = None
        self.startPoint = 0
        self.endPoint = 0
        self.initUI()


    def initUI(self):
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

        image = Image.open("street.png")
        resizedImage = image.resize((800, 500))
        imageTk = ImageTk.PhotoImage(resizedImage)
        im = self.tk.Label(self.root, image=imageTk, bg="lightgreen")
        im.grid(row=0, column=0, columnspan=5, sticky="")

        currentInstruction = self.tk.Label(self.root, text=str(self.instruction), bg="lightgreen", foreground="black", width=30, height=1)
        currentInstruction.grid(row=1, column=0, sticky="w")

        button = self.tk.Button(self.root, text="Start")
        button.grid(row=1, column=1, sticky="")

        entry = self.tk.Entry(self.root)
        self.entry = entry
        #entry.pack()
        # Füge Event-Binding für die Enter-Taste hinzu
        entry.bind("<Return>", self.get_input)
        # Setze den Fokus auf das Entry-Widget, damit die Enter-Taste funktioniert
        entry.focus_set()
        entry.grid(row=1, column=2, sticky="")


        speed = self.tk.Label(self.root, text="Speed: " + str(self.speed) + " (km/h)", foreground="black", bg="lightgreen", width=20, height=1)
        speed.grid(row=1, column=3, sticky="")

        currentDrivenDistance = self.tk.Label(self.root, text="Distance: " + str(self.dist) + " m", foreground="black", bg="lightgreen")
        currentDrivenDistance.grid(row=1, column=4, sticky="")

        self.root.mainloop()

    def drawRouteInMap(self,coordx,coordy):
        image = Image.open("street.png")

        # Erstellen Sie ein Zeichen-Objekt
        draw = ImageDraw.Draw(image)
        # Definieren Sie Ihre Route als Liste von Koordinaten (x, y)
        route = [(40, 0), (100, 200), (100, 300), (100, 400)]  # Beispielkoordinaten
        # Zeichnen Sie die Route als Linien
        draw.line(route, fill=(255, 0, 0), width=3)  # Rote Linienbreite 3
        # Definieren Sie die Koordinaten des Punktes (x, y)
        point_coordinates = (100, 200)  # Beispielkoordinaten

        # Größe des Punkts
        point_size = 2

        # Zeichnen Sie einen größeren Punkt
        for x in range(point_coordinates[0] - point_size, point_coordinates[0] + point_size + 1):
            for y in range(point_coordinates[1] - point_size, point_coordinates[1] + point_size + 1):
                draw.point((x, y), fill=(255, 0, 0))  # Roter Punkt
        # Speichern Sie das bearbeitete Bild
        image.save('map_with_route.png')
        image = Image.open("map_with_route.png")
        # image = Image.open("street.png")

        resizedImage = image.resize((800, 500))
        imageTk = ImageTk.PhotoImage(resizedImage)
        im = self.tk.Label(self.root, image=imageTk, bg="lightgreen")
        im.grid(row=0, column=0, columnspan=5, sticky="")

    def updateUi(self):
        return

    def get_input(self,event):
        user_input = self.entry.get()  # Hole die Eingabe aus dem Entry-Widget
        if self.instruction == instructionStartPoint:
            self.instruction = instructionEndPoint
            self.startPoint = user_input
        elif self.instruction == instructionEndPoint:
            self.startPoint = user_input
        else:
            print("Benutzereingabe passt nicht:", user_input)

if __name__ == "__main__":
    ui = userInterface()
    #while(True):
    #    ui.drawRouteInMap(1,2)