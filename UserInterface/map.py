import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw
from .car import Car


class Map:
    def __init__(self):
        self.default_map = None
        self.current_map = None
        self.car = Car()
        self.min_pixel_value_for_drawing = 0.3
        self.init_map()

    def init_map(self):
        self.default_map = Image.open("UserInterface/street_with_node_nummeration.png").resize((800, 500))

    def draw_route_in_map(self, route_cords):  # function to draw route in map
        print("drawRoute")
        img = cv2.imread("UserInterface/street_with_node_nummeration.png", cv2.COLOR_BGR2GRAY)
        for i in range(len(route_cords)):
            if i + 1 < len(route_cords):
                first = route_cords[i] - 1
                next = route_cords[i + 1] - 1
                cv2.line(img, (self.car.coordinates_of_all_node[first][0], self.car.coordinates_of_all_node[first][1]),
                         (self.car.coordinates_of_all_node[next][0], self.car.coordinates_of_all_node[next][1]),
                         (0, 0, 255), 1)

        cv2.imwrite("UserInterface/map_with_route.png", img)
        self.current_map = Image.open("UserInterface/map_with_route.png").resize((800, 500))

    def position_car_on_map(self, start, end):
        self.car.initialize_car(start, end)
        map = cv2.imread("UserInterface/map_with_route.png", cv2.IMREAD_UNCHANGED)
        # Erstelle einen leeren Alphakanal mit denselben Dimensionen wie das Bild
        height, width = map.shape[:2]
        alpha_channel = np.ones((height, width),
                                dtype=np.uint8) * 255  # Fülle den Alphakanal mit voller Transparenz (255)

        # Füge den Alphakanal dem Bild hinzu
        map = cv2.merge((map, alpha_channel))

        car_height, car_width = self.car.picture_of_car_rotated.shape[:2]

        x_position = self.car.x_position - int(car_width / 2)
        y_position = self.car.y_position - int(car_height / 2)

        # Platzieren des Auto-Bildes auf dem Hauptbild an den angegebenen Koordinaten
        map[y_position:y_position + car_height, x_position:x_position + car_width] = self.car.picture_of_car_rotated

        # Speichern des resultierenden Bildes mit dem platzierten Auto
        cv2.imwrite("UserInterface/map_with_route_and_car_position.png", map)
        self.current_map = Image.open("UserInterface/map_with_route_and_car_position.png").resize((800, 500))

    def update_rotation_of_car(self, current_rotation):
        print(current_rotation)
        match current_rotation:
            case 0:
                self.car.picture_of_car_rotated = cv2.rotate(self.car.picture_of_car_rotated, cv2.ROTATE_90_COUNTERCLOCKWISE)
                self.car.rotation -= 1
                if self.car.rotation < 0:
                    self.car.rotation = 3
            case 1:
                self.car.picture_of_car_rotated = cv2.rotate(self.car.picture_of_car_rotated, cv2.ROTATE_90_CLOCKWISE)
                self.car.rotation += 1
                if self.car.rotation > 3:
                    self.car.rotation = 0

    def update_position_of_car_on_map(self, driven_distance):

        pixel_to_add = round(driven_distance*100 * self.min_pixel_value_for_drawing)
        self.car.add_distance_to_coordinates_of_car(pixel_to_add)
        map = cv2.imread("UserInterface/map_with_route.png", cv2.IMREAD_UNCHANGED)
        # Erstelle einen leeren Alphakanal mit denselben Dimensionen wie das Bild
        height, width = map.shape[:2]
        alpha_channel = np.ones((height, width),
                                dtype=np.uint8) * 255  # Fülle den Alphakanal mit voller Transparenz (255)

        # Füge den Alphakanal dem Bild hinzu
        map = cv2.merge((map, alpha_channel))

        car_height, car_width = self.car.picture_of_car_rotated.shape[:2]

        x_position = self.car.x_position - int(car_width / 2)
        y_position = self.car.y_position - int(car_height / 2)
        print(x_position, y_position)

        # Platzieren des Auto-Bildes auf dem Hauptbild an den angegebenen Koordinaten
        map[y_position:y_position + car_height, x_position:x_position + car_width] = self.car.picture_of_car_rotated

        # Speichern des resultierenden Bildes mit dem platzierten Auto
        cv2.imwrite("UserInterface/map_with_route_and_car_position.png", map)
        self.current_map = Image.open("UserInterface/map_with_route_and_car_position.png").resize((800, 500))

    def center_car_to_node(self, node):
        map = cv2.imread("UserInterface/map_with_route.png", cv2.IMREAD_UNCHANGED)
        # Erstelle einen leeren Alphakanal mit denselben Dimensionen wie das Bild
        height, width = map.shape[:2]
        alpha_channel = np.ones((height, width),
                                dtype=np.uint8) * 255  # Fülle den Alphakanal mit voller Transparenz (255)

        # Füge den Alphakanal dem Bild hinzu
        map = cv2.merge((map, alpha_channel))

        car_height, car_width = self.car.picture_of_car_rotated.shape[:2]
        self.car.x_position = self.car.coordinates_of_all_node[node - 1][0]
        self.car.y_position = self.car.coordinates_of_all_node[node - 1][1]
        x_position = self.car.x_position - int(car_width / 2)
        y_position = self.car.y_position - int(car_height / 2)
        print(self.car.x_position, self.car.y_position)

        # Platzieren des Auto-Bildes auf dem Hauptbild an den angegebenen Koordinaten
        map[y_position:y_position + car_height, x_position:x_position + car_width] = self.car.picture_of_car_rotated

        # Speichern des resultierenden Bildes mit dem platzierten Auto
        cv2.imwrite("UserInterface/map_with_route_and_car_position.png", map)
        self.current_map = Image.open("UserInterface/map_with_route_and_car_position.png").resize((800, 500))


if __name__ == "__main__":
    map = Map()
    map.draw_route_in_map(0)
