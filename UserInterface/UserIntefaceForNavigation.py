import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import cv2
import numpy as np
from .UserInterfaceConfig import *
from .StreetSign import *


# ui class
class Userinterface:
    def __init__(self):
        self.tk_root_window = tk.Tk()  # tkinter window of application
        self.tk = tk  # tkinter object
        self.current_instruction = instruction_start_point  # instruction
        self.tk_current_instruction_window = 0  # tkinter instruction in application
        self.speed = 0
        self.tk_current_speed_window = 0  # tkinter speed in application
        self.distance = 0
        self.distance_to_drive = 0
        self.tk_current_driven_distance_window = 0  # tkinter distance in application
        self.street_sign = streetSign()
        self.tk_entry_for_input = None  # tkinter input window
        self.start_point = 0
        self.end_point = 0
        self.user_input_check_if_ready = False  # bool to check if start and end point are given
        self.tk_image_window = 0  # tkinter map in application
        self.end_application_check = False
        self.tk_button_window = 0  # tkinter startbutton in application

    def init_ui(self):
        print("init Gui started")
        # Setze die Fenstergröße auf 1000x530 Pixel
        self.tk_root_window.geometry("1000x530")
        self.tk_root_window.maxsize(800, 700)
        # Ändern der Hintergrundfarbe auf hellgrün
        self.tk_root_window.configure(bg="#45BD6A")
        self.tk_root_window.title("Navigation")

        # setting window in rows and columns
        self.tk_root_window.columnconfigure(0, weight=1)
        self.tk_root_window.columnconfigure(1, weight=1)
        self.tk_root_window.columnconfigure(2, weight=1)
        self.tk_root_window.columnconfigure(3, weight=1)
        self.tk_root_window.columnconfigure(4, weight=1)

        # root.rowconfigure(0,weight=2)
        self.tk_root_window.rowconfigure(0, weight=5)
        self.tk_root_window.rowconfigure(1, weight=2)

        # initializing every cell
        for i in range(2):
            for j in range(5):
                if i != 0:
                    # frame = tk.Frame(root, borderwidth=1, relief="solid", width=160, height=50,bg="lightgreen")
                    frame = self.tk.Frame(self.tk_root_window, width=200, height=50, bg="lightgreen")
                    frame.grid(row=i, column=j)
                else:
                    if j == 0 and i == 0:
                        # frame = tk.Frame(root, borderwidth=1, relief="solid", width=800, height=500,bg="lightgreen")
                        frame = self.tk.Frame(self.tk_root_window, width=1000, height=500, bg="lightgreen")
                        frame.grid(row=i, column=j, columnspan=5)

        # setting default map in application
        image = Image.open("UserInterface/street_with_node_nummeration.png")
        resized_image = image.resize((800, 500))
        image_tk = ImageTk.PhotoImage(resized_image)
        self.tk_image_window = self.tk.Label(self.tk_root_window, image=image_tk, bg="lightgreen")
        self.tk_image_window.grid(row=0, column=0, columnspan=5, sticky="")

        # setting instruction window in application
        self.tk_current_instruction_window = self.tk.Label(self.tk_root_window, text=str(self.current_instruction),
                                                           bg="lightgreen",
                                                           foreground="black", width=30, height=1)
        self.tk_current_instruction_window.grid(row=1, column=0, sticky="w")

        # setting button window in application
        self.tk_button_window = self.tk.Button(self.tk_root_window, text="Start", command=self.start_button_pressed)
        self.tk_button_window.grid(row=1, column=1, sticky="")

        # setting input window in application
        entry = self.tk.Entry(self.tk_root_window)
        self.tk_entry_for_input = entry
        # Füge Event-Binding für die Enter-Taste hinzu
        entry.bind("<Return>", self.get_input)
        # Setze den Fokus auf das Entry-Widget, damit die Enter-Taste funktioniert
        entry.focus_set()
        entry.grid(row=1, column=2, sticky="")

        # setting speed window in application
        self.tk_current_speed_window = self.tk.Label(self.tk_root_window, text="Speed: " + str(self.speed) + " (km/h)",
                                                     foreground="black",
                                                     bg="lightgreen", width=20, height=1)
        self.tk_current_speed_window.grid(row=1, column=3, sticky="")

        # setting distance window in application
        self.tk_current_driven_distance_window = self.tk.Label(self.tk_root_window,
                                                               text="Distance: " + str(self.distance) + " m",
                                                               foreground="black", bg="lightgreen")
        self.tk_current_driven_distance_window.grid(row=1, column=4, sticky="")

        # function to be called after closing application
        self.tk_root_window.protocol("WM_DELETE_WINDOW", self.set_closed_programm)

        # starting ui
        self.tk_root_window.mainloop()

    def set_closed_programm(self):  # function to close full application and the navigation thread
        self.end_application_check = True
        self.tk_root_window.destroy()

    def get_closed_program_bool(self):  # function to return bool if application has to be closed
        return self.end_application_check

    def get_initial_orientation_of_car_on_map(self, route):  # function to get initial orientation of car on the map
        match self.start_point:
            case 1, 2:  # if node 1 or 2
                return 4
            case 3, 7:  # if node 3 or 7
                return 1
            case 11, 12:  # if node 11 or 12
                return 2
            case 6, 10:  # if node 6 or 10
                return 0
            case _:
                node_coords = self.load_node_coords()  # 0 counter   1 clockwise    2 180grad
                current_node_index = route[0]
                next_node_index = route[1]
                current_node = node_coords[current_node_index - 1]
                next_node = node_coords[next_node_index - 1]
                if current_node[0] == next_node[0]:
                    if current_node[1] < next_node[1]:
                        return 2
                    else:
                        return 4
                elif current_node[1] == next_node[1]:
                    if current_node[0] < next_node[0]:
                        return 1
                    elif current_node[0] > next_node[0]:
                        return 0
                return 4

    def position_car_on_map(self, route):  # function to position car on map
        car = cv2.imread("UserInterface/car2.png", cv2.IMREAD_UNCHANGED)
        car_resized = cv2.resize(car, (10, 20))
        rotation_of_car = self.get_initial_orientation_of_car_on_map(route)
        car_resized = self.get_rotated_car(rotation_of_car, car_resized)
        cv2.imwrite("UserInterface/car_current_orientation.png", car_resized)

        map = cv2.imread("UserInterface/map_with_route.png", cv2.IMREAD_UNCHANGED)
        # Erstelle einen leeren Alphakanal mit denselben Dimensionen wie das Bild
        height, width = map.shape[:2]
        alpha_channel = np.ones((height, width),
                                dtype=np.uint8) * 255  # Fülle den Alphakanal mit voller Transparenz (255)

        # Füge den Alphakanal dem Bild hinzu
        map = cv2.merge((map, alpha_channel))

        node_coords_in_map = self.load_node_coords()

        car_height, car_width = car_resized.shape[:2]

        x_position = node_coords_in_map[self.start_point - 1][0] - int(car_width / 2)
        y_position = node_coords_in_map[self.start_point - 1][1] - int(car_height / 2)

        # Platzieren des Auto-Bildes auf dem Hauptbild an den angegebenen Koordinaten
        map[y_position:y_position + car_height, x_position:x_position + car_width] = car_resized

        # Speichern des resultierenden Bildes mit dem platzierten Auto
        cv2.imwrite("UserInterface/map_with_route_and_car_position.png", map)
        updated_image = Image.open("UserInterface/map_with_route_and_car_position.png")
        resized_image = updated_image.resize((800, 500))
        imageTk = ImageTk.PhotoImage(resized_image)
        self.tk_image_window.config(image=imageTk)
        self.tk_image_window.image = imageTk

    def update_position_of_car_on_map(self, current_node, next_node, current_rotation_from_mpu6050, current_cost,
                                      cost_between_nodes):  # function to update car position during runtime
        car = cv2.imread("UserInterface/car_current_orientation.png", cv2.IMREAD_UNCHANGED)
        car_resized = cv2.resize(car, (10, 20))
        car_resized = self.get_rotated_car(current_rotation_from_mpu6050, car_resized)

        pixels_between_two_nodes_x = 0
        pixels_between_two_nodes_y = 0
        pixel_of_one_cost = 0
        current_pixel_cost_on_map = 0
        y_position = 0
        x_position = 0

        if current_node[0] == next_node[0]:
            x_position = int(current_node[0])
            if current_node[1] > next_node[1]:
                pixels_between_two_nodes_y = next_node[1] - current_node[1]
            elif current_node[1] < next_node[1]:
                pixels_between_two_nodes_y = next_node[1] - current_node[1]
            pixel_of_one_cost = pixels_between_two_nodes_y / cost_between_nodes
            current_pixel_cost_on_map = pixel_of_one_cost * current_cost
            y_position = int(current_node[1] + current_pixel_cost_on_map)

        if current_node[1] == next_node[1]:
            y_position = int(current_node[1])
            if current_node[0] > next_node[0]:
                pixels_between_two_nodes_x = next_node[0] - current_node[0]
            elif current_node[0] < next_node[0]:
                pixels_between_two_nodes_x = next_node[0] - current_node[0]
            pixel_of_one_cost = pixels_between_two_nodes_x / cost_between_nodes
            current_pixel_cost_on_map = pixel_of_one_cost * current_cost
            x_position = int(current_node[0] + current_pixel_cost_on_map)

        map = cv2.imread("UserInterface/map_with_route.png", cv2.IMREAD_UNCHANGED)
        # Erstelle einen leeren Alphakanal mit denselben Dimensionen wie das Bild
        height, width = map.shape[:2]
        alpha_channel = np.ones((height, width),
                                dtype=np.uint8) * 255  # Fülle den Alphakanal mit voller Transparenz (255)

        # Füge den Alphakanal dem Bild hinzu
        map = cv2.merge((map, alpha_channel))

        car_height, car_width = car_resized.shape[:2]

        x_position = x_position - int(car_width / 2)
        y_position = y_position - int(car_height / 2)

        # Platzieren des Auto-Bildes auf dem Hauptbild an den angegebenen Koordinaten
        map[y_position:y_position + car_height, x_position:x_position + car_width] = car_resized

        # Speichern des resultierenden Bildes mit dem platzierten Auto
        cv2.imwrite("UserInterface/map_with_route_and_car_position.png", map)

        updated_image = Image.open("UserInterface/map_with_route_and_car_position.png")
        resized_image = updated_image.resize((800, 500))
        imageTk = ImageTk.PhotoImage(resized_image)
        self.tk_image_window.config(image=imageTk)
        self.tk_image_window.image = imageTk

    @staticmethod
    def get_rotated_car(standing_of_car_on_map, car_resized):  # function to rotate car
        match standing_of_car_on_map:
            case 0:
                car_resized = cv2.rotate(car_resized, cv2.ROTATE_90_COUNTERCLOCKWISE)
            case 1:
                car_resized = cv2.rotate(car_resized, cv2.ROTATE_90_CLOCKWISE)
            case 2:
                car_resized = cv2.rotate(car_resized, cv2.ROTATE_180)

        return car_resized

    @staticmethod
    def load_node_coords():  # function to load node coordinates
        return np.loadtxt("UserInterface/nodeCordOnMap.txt").astype(int)

    def draw_route_in_map(self, route_ccoords):  # function to draw route in map
        print("drawRoute")
        img = cv2.imread("UserInterface/street_with_node_nummeration.png", cv2.COLOR_BGR2GRAY)
        nodeCoordsInMap = self.load_node_coords()
        for i in range(len(route_ccoords)):
            if i + 1 < len(route_ccoords):
                first = route_ccoords[i] - 1
                next = route_ccoords[i + 1] - 1
                cv2.line(img, (nodeCoordsInMap[first][0], nodeCoordsInMap[first][1]),
                         (nodeCoordsInMap[next][0], nodeCoordsInMap[next][1]), (0, 0, 255), 1)
        # cv2.imshow("test", img)
        cv2.imwrite("UserInterface/map_with_route.png", img)
        # Bild in das Tkinter Label laden und aktualisieren
        updated_image = Image.open("UserInterface/map_with_route.png")
        resized_image = updated_image.resize((800, 500))
        imageTk = ImageTk.PhotoImage(resized_image)
        self.tk_image_window.config(image=imageTk)
        self.tk_image_window.image = imageTk

    def update_ui_to_start_again(self):  # function to restart navigation
        self.tk_button_window.config(text="Start", command=self.start_button_pressed)
        image = Image.open("UserInterface/street_with_node_nummeration.png")
        resizedImage = image.resize((800, 500))
        imageTk = ImageTk.PhotoImage(resizedImage)
        self.tk_image_window.config(image=imageTk)
        self.tk_image_window.image = imageTk
        self.current_instruction = instruction_start_point
        self.update_instruction_in_gui()
        self.user_input_check_if_ready = False
        self.set_distance(0)
        return

    def get_input(self, event):  # function to get the input from user
        userInput = self.tk_entry_for_input.get()  # Hole die Eingabe aus dem Entry-Widget
        print(userInput)
        if self.current_instruction == instruction_start_point or self.current_instruction == instruction_wrong_input_one:
            self.current_instruction = instruction_end_point
            self.start_point = self.get_driving_point_from_input_and_convert_it_to_a_number(userInput)
        elif self.current_instruction == instruction_end_point or self.current_instruction == instruction_wrong_input_two:
            self.end_point = self.get_driving_point_from_input_and_convert_it_to_a_number(userInput)
            self.current_instruction = instruction_wait_for_start_button
        else:
            print("Benutzereingabe passt nicht:", userInput)
        if self.start_point == 13:
            self.current_instruction = instruction_wrong_input_one
        elif self.end_point == 13:
            self.current_instruction = instruction_wrong_input_two

        self.update_instruction_in_gui()
        self.tk_entry_for_input.delete(0, self.tk.END)

    def get_start_point_for_navigation(self):  # function to get starting point of navigation
        return int(self.start_point)

    def get_end_point_for_navigation(self):  # function to get end point of navigation
        return int(self.end_point)

    def set_distance(self, cost):  # function to set new distance in ui
        self.distance = float(cost)
        self.distance_to_drive = self.distance
        self.update_driven_distance(self.distance)

    def calc_distance_to_drive(self, dist):  # function to calculate current distance to drive
        self.distance_to_drive = self.distance - dist
        # new_cost = self.dist - range_to_drive
        self.update_driven_distance(self.distance_to_drive)

    def update_instruction_in_gui(self):  # function to update instruction in ui
        self.tk_current_instruction_window.config(text=self.current_instruction)

    def update_speed(self, currentSpeed):  # function to update speed in ui
        self.speed = currentSpeed
        self.tk_current_speed_window.config(text="Speed: " + str(currentSpeed) + " (km/h)")

    def update_driven_distance(self, dist):  # function to update distance in ui
        # self.dist = dist
        rounded_dist = round(dist, 1)
        self.tk_current_driven_distance_window.config(text="Distance: " + str(rounded_dist) + " m")

    def update_button(self):  # function to set new button function
        if self.current_instruction == instruction_drive:
            self.tk_button_window.config(text="End", command=self.end_button_pressed)
        elif self.current_instruction == instruction_end_driving:
            # self.instruction = instructionStartPoint
            self.update_ui_to_start_again()

    def start_button_pressed(self):  # function for start button
        self.user_input_check_if_ready = True
        self.current_instruction = instruction_drive
        self.update_instruction_in_gui()
        self.update_button()

    def end_button_pressed(self):  # function for end button
        self.current_instruction = instruction_end_driving
        self.update_button()

    def get_driving_instructions_from_route(self, route):  # function to get driving instructions from given route
        drivingInstructions = []
        nodeCoordsInMap = self.load_node_coords()
        current = 0
        prev = 0
        next = 0
        for i in range(0, len(route)):
            if i + 1 < len(route):
                if i == 0:
                    prev = route[i] - 1
                else:
                    prev = current
                current = route[i] - 1
                next = route[i + 1] - 1
                drivingInstructions.append(
                    self.calc_instruction(nodeCoordsInMap[prev], nodeCoordsInMap[current], nodeCoordsInMap[next]))
        return drivingInstructions

    def set_instruction_to_wait_for_end_button(self):
        self.current_instruction = instruction_end_driving
        self.update_instruction_in_gui()

    def calc_instruction(self, prev, cur, next):  # function to calculate instruction where to drive for the car
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

    @staticmethod
    def get_driving_point_from_input_and_convert_it_to_a_number(input):  # function to get node number where to drive after input
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
            case _:
                numb = 13
        return numb


if __name__ == "__main__":
    ui = Userinterface()
    ui.init_ui()
    # while(True):
    #    ui.drawRouteInMap(1,2)
