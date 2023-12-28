import Tkinter as tk
from pillow import Image,ImageTk, ImageDraw
import cv2
import numpy as np
from Routing.routing import dijkstra

speed = 10
dist = 10

if __name__ == "__main__":
    img = cv2.imread("street.png", cv2.COLOR_BGR2GRAY)
    nodeCoordsInMap = np.loadtxt("nodeCordOnMap.txt").astype(int)
    route, cost = dijkstra(2,11,1)
    for i in range(len(route)):
        if i+1 < len(route):
            first = route[i]-1
            next = route[i+1]-1
            cv2.line(img, (nodeCoordsInMap[first][0], nodeCoordsInMap[first][1]), (nodeCoordsInMap[next][0], nodeCoordsInMap[next][1]), (0, 0, 255), 1)
    img = cv2.resize(img, (1000, 700))
    cv2.imwrite("map_with_route.png",img)
    #cv2.imshow("test", img)
    # Erstelle ein Hauptfenster
    root = tk.Tk()

    root.geometry("1000x750")
    root.maxsize(2000, 2000)

    root.configure(bg="#45BD6A")
    root.title("Navigation")

    root.columnconfigure(0,weight=1)
    root.columnconfigure(1,weight=1)
    root.columnconfigure(2,weight=1)
    root.columnconfigure(3,weight=1)
    root.columnconfigure(4,weight=1)


    #root.rowconfigure(0,weight=2)
    root.rowconfigure(0,weight=5)
    root.rowconfigure(1,weight=2)



    for i in range(2):
        for j in range(5):
            if i != 0:
                #frame = tk.Frame(root, borderwidth=1, relief="solid", width=160, height=50,bg="lightgreen")
                frame = tk.Frame(root, width=200, height=50, bg="lightgreen")
                frame.grid(row=i, column=j)
            else:
                if j == 0 and i == 0:
                    #frame = tk.Frame(root, borderwidth=1, relief="solid", width=800, height=500,bg="lightgreen")
                    frame = tk.Frame(root, width=1000, height=700, bg="lightgreen")
                    frame.grid(row=i, column=j, columnspan=5)

    #imageSign = Image.open("../TrafficSigns/stopSign.png")
    #resizedImageSign = imageSign.resize((30,30))
    #imageTkSign = ImageTk.PhotoImage(resizedImageSign)
    #imSign = tk.Label(root,image=imageTkSign,bg="lightgreen")
    #imSign.grid(row=0,column=4,sticky="")
    #img = cv2.imread("street.png")

    #image.save('map_with_route.png')
    image = Image.open("map_with_route.png")
    #image = Image.open("street.png")
    #image = img
    resizedImage = image.resize((700,540))
    imageTk = ImageTk.PhotoImage(image)
    im = tk.Label(root,image=imageTk,bg="lightgreen")
    im.grid(row=0,column=0,columnspan=5,sticky="")




    currentInstruction = tk.Label(root, text="Bitte waehle Startpunkt",bg="lightgreen", foreground = "black", width=20,height=1)
    currentInstruction.grid(row=1, column=0,sticky="w")

    button = tk.Button(root, text="Start")
    button.grid(row=1, column=1, sticky="")

    entry = tk.Entry(root)
    entry.grid(row=1,column=2,sticky="")

    speed = tk.Label(root, text="Speed: "+ str(speed)+" (km/h)", foreground = "black",bg="lightgreen", width=20,height=1)
    speed.grid(row=1, column=3, sticky="")

    currentDrivenDistance = tk.Label(root, text="Distance: "+str(dist)+" m", foreground = "black",bg="lightgreen")
    currentDrivenDistance.grid(row=1, column=4, sticky="")



    root.mainloop()

