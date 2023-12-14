import tkinter as tk
from PIL import Image,ImageTk, ImageDraw

speed = 10
dist = 10

if __name__ == "__main__":

    # Erstelle ein Hauptfenster
    root = tk.Tk()
    # Setze die Fenstergröße auf 800x600 Pixel
    root.geometry("1000x530")
    root.maxsize(800, 700)
    # Ändern Sie die Hintergrundfarbe auf hellgrün
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
                    frame = tk.Frame(root, width=1000, height=500, bg="lightgreen")
                    frame.grid(row=i, column=j, columnspan=5)

    #imageSign = Image.open("../TrafficSigns/stopSign.png")
    #resizedImageSign = imageSign.resize((30,30))
    #imageTkSign = ImageTk.PhotoImage(resizedImageSign)
    #imSign = tk.Label(root,image=imageTkSign,bg="lightgreen")
    #imSign.grid(row=0,column=4,sticky="")
    #img = cv2.imread("street.png")
    image = Image.open("street.png")

    # Erstellen Sie ein Zeichen-Objekt
    draw = ImageDraw.Draw(image)
    # Definieren Sie Ihre Route als Liste von Koordinaten (x, y)
    route = [(40,0),(100, 200), (100, 300), (100, 400)]  # Beispielkoordinaten
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
    #image = Image.open("street.png")

    resizedImage = image.resize((800,500))
    imageTk = ImageTk.PhotoImage(resizedImage)
    im = tk.Label(root,image=imageTk,bg="lightgreen")
    im.grid(row=0,column=0,columnspan=5,sticky="")




    currentInstruction = tk.Label(root, text="Bitte wähle Startpunkt",bg="lightgreen", foreground = "black", width=30,height=1)
    currentInstruction.grid(row=1, column=0,sticky="w")

    button = tk.Button(root, text="Start")
    button.grid(row=1, column=1, sticky="")

    entry = tk.Entry(root)
    entry.grid(row=1,column=2,sticky="")

    speed = tk.Label(root, text="Speed: "+ str(speed)+" (km/h)", foreground = "black",bg="lightgreen", width=20,height=1)
    speed.grid(row=1, column=3, sticky="")

    currentDrivenDistance = tk.Label(root, text="Distance: "+str(dist)+" m", foreground = "black",bg="lightgreen")
    currentDrivenDistance.grid(row=1, column=4, sticky="")

    # Hier können Sie Widgets in die Zellen des Grid-Layouts legen

    root.mainloop()

