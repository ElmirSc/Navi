import cv2
import numpy as np
from .car_config import *

class Car:
    def __init__(self):
        self.x_position = 0
        self.y_position = 0
        self.picture_of_car = None
        self.picture_of_car_rotated = None
        self.rotation = None
        self.coordinates_of_all_node = np.loadtxt("UserInterface/node_cordinates_on_map.txt").astype(int)
        self.drives_true_route = True

    def initialize_car(self, start_node, next_node):
        self.x_position = self.coordinates_of_all_node[start_node-1][0]
        self.y_position = self.coordinates_of_all_node[start_node-1][1]
        self.picture_of_car = cv2.imread("UserInterface/car2.png", cv2.IMREAD_UNCHANGED)
        self.picture_of_car = cv2.resize(self.picture_of_car, (10, 20))
        self.rotation = self.calculate_rotation(start_node, next_node)
        self.rotate_car()

    def calculate_rotation(self, start_node, next_node):
        match start_node:
            case 1, 2:  # if node 1 or 2
                return north_orientation
            case 3, 7:  # if node 3 or 7
                return east_orientation
            case 11, 12:  # if node 11 or 12
                return south_orientation
            case 6, 10:  # if node 6 or 10
                return west_orientation
            case _:
                # 0 counter   1 clockwise    2 180grad
                current_node_coordinates = self.coordinates_of_all_node[start_node - 1]
                next_node_coordinates = self.coordinates_of_all_node[next_node - 1]
                if current_node_coordinates[0] == next_node_coordinates[0]:
                    if current_node_coordinates[1] < next_node_coordinates[1]:
                        return south_orientation
                    else:
                        return north_orientation
                elif current_node_coordinates[1] == next_node_coordinates[1]:
                    if current_node_coordinates[0] < next_node_coordinates[0]:
                        return east_orientation
                    elif current_node_coordinates[0] > next_node_coordinates[0]:
                        return west_orientation
                return north_orientation

    def rotate_car(self):
        match self.rotation:
            case 0:
                self.picture_of_car_rotated = self.picture_of_car
            case 2:
                self.picture_of_car_rotated = cv2.rotate(self.picture_of_car, cv2.ROTATE_180)
            case 1:
                self.picture_of_car_rotated = cv2.rotate(self.picture_of_car, cv2.ROTATE_90_CLOCKWISE)
            case 3:
                self.picture_of_car_rotated = cv2.rotate(self.picture_of_car, cv2.ROTATE_90_COUNTERCLOCKWISE)

    def add_distance_to_coordinates_of_car(self,distance, map_height, map_width):
        match self.rotation:
            case 0: #norden
                self.y_position = self.y_position - distance
                if self.y_position < 0:
                    self.y_position = 0
            case 2:#süden
                self.y_position = self.y_position + distance
                if self.y_position > map_height:
                    self.y_position = map_height - 1
            case 1:#osten
                self.x_position = self.x_position + distance
                if self.x_position > map_width:
                    self.x_position = map_width - 1
            case 3:#westen
                self.x_position = self.x_position - distance
                if self.x_position < 0:
                    self.x_position = 0
