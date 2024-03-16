import threading

import numpy as np
from UserInterface.userinteface_for_navigation import Userinterface
from Routing.routing import dijkstra, arc_list, node_list
from Navigation.navigation_config import *
from threading import Thread
from Navigation.server import Server


# class which implements the whole state manager for the navigation
class Navigation:
    def __init__(self):
        self.ui = Userinterface()  # ui object
        self.server = Server("172.20.10.5", 5556)  # server object
        self.current_state_of_app = before_navigation_state  # initial state of the application
        self.routing_cost = 0  # total routing cost
        self.thread_one = 0  # thread object for start application without ui
        self.factor_for_real_distance = 1  # factor for calculating the real distance
        self.current_node = 0  # current node where car is driving away to next node
        self.next_node = 0  # next node where the car is driving
        self.node_coords_list = np.loadtxt("UserInterface/node_cordinates_on_map.txt").astype(
            int)  # list of node coordinates on map
        self.all_driving_instructions = None
        self.next_instruction = None
        self.thread_lock = threading.Lock()
        self.prev_distance = 0
        self.end_node_x_cords = 0
        self.end_node_y_cords = 0
        self.next_node_x = 0
        self.next_node_y = 0
        self.wait_for_crossing = False
        self.crossing_updated = False
        self.straight_updated = False
        self.is_at_node = False

    @staticmethod
    def get_route_from_algorithm(start_node, end_node):  # function to calculate the route and its full cost
        return dijkstra(start_node, end_node, 1)

    def calc_real_range_from_cost_and_factor(self):  # calculating real range if the real driving area is bigger
        return self.factor_for_real_distance * self.routing_cost

    def start_ui(self):  # function to start the ui of the application
        self.ui.init_ui()

    def init_navigation(self):  # function to initialize the full application
        self.server.create_socket()
        self.server.set_socket_to_listen_mode()

        self.thread_one = Thread(target=self.start_application)
        self.thread_one.start()
        self.start_ui()
        self.thread_one.join()

    def set_to_end_of_driving(self):
        self.server.send_data(0)
        self.current_state_of_app = driving_end_state
        self.ui.update_speed(0)
        self.ui.set_distance(0)
        self.server.driven_distance = 0

    def start_application(self):  # function to start the state manager
        try:
            route = None
            while True:
                self.thread_lock.acquire()
                try:
                    if self.ui.end_application_check:  # zum schliessen des ganzen programms
                        break
                    elif not self.ui.user_input_check_if_ready:  # erst wenn Input fertig ist wird state gesetzt
                        self.current_state_of_app = before_navigation_state

                    match self.current_state_of_app:
                        case 1:  # state before input is ready
                            if self.ui.user_input_check_if_ready:
                                self.current_state_of_app = after_input_state
                        case 2:  # state after input to get route and cost and initialize the map in the ui

                            route, cost = self.get_route_from_algorithm(
                                self.ui.get_start_point_for_navigation(), self.ui.get_end_point_for_navigation())
                            self.set_x_and_y_coordinates_for_end_node(route)

                            self.all_driving_instructions = self.ui.get_driving_instructions_from_route(route)
                            instructions_to_send = self.all_driving_instructions[:]
                            self.process_driving_instructions()

                            self.update_nodes_calc_routing_cost_and_get_next_instruction(route, cost)
                            self.set_distance_and_draw_route_in_map(route)
                            route.reverse()
                            route.pop()

                            if self.server.has_connection_to_client or self.server.accept_connection():
                                self.current_state_of_app = driving_state

                            self.server.send_data(instructions_to_send)
                        case 3:  # driving state where distance, speed and car location gets updated
                            print("x-position:", self.ui.map.car.x_position)
                            print("y-position:", self.ui.map.car.y_position)
                            self.check_and_handle_the_data_from_server_socket()
                            self.update_ui_with_current_distance_and_speed()
                            self.check_if_route_ended()
                            self.update_car_rotation()
                            route = self.check_if_car_is_at_node_position(route)
                            self.update_car_position()

                            #route = self.check_if_car_is_at_other_node_position(route)
                            self.ui.update_map()

                        case 4:  # end state
                            self.update_ui_to_start_next_route()
                finally:
                    self.thread_lock.release()
        except KeyboardInterrupt:
            print("progamm closed!")

    def update_nodes_to_get_new_next_and_current_nodes(self, new_current_node,
                                                       new_next_node):  # function get set the next node to current node and to set a new next node
        self.next_node = new_next_node
        self.current_node = new_current_node

    def check_if_route_ended(self):
        if abs(self.ui.map.car.x_position - self.end_node_x_cords) <= 2 and abs(
                self.ui.map.car.y_position - self.end_node_y_cords) <= 2:
            self.set_to_end_of_driving()

    def check_and_handle_the_data_from_server_socket(self):
        self.server.receive_data()
        self.server.handle_data()

    def update_ui_with_current_distance_and_speed(self):
        self.ui.calc_distance_to_drive(self.server.driven_distance)

        self.ui.update_speed(self.server.current_speed)

    def set_x_and_y_coordinates_for_end_node(self, route):
        self.end_node_x_cords = self.ui.map.car.coordinates_of_all_node[route[len(route) - 1] - 1][0]
        self.end_node_y_cords = self.ui.map.car.coordinates_of_all_node[route[len(route) - 1] - 1][1]

    def get_cost_for_driving_in_node(self, instruction):
        match instruction:
            case "g":
                return 2
            case "r":
                return 1.6
            case "l":
                return 1.6
            case _:
                return 0

    def calc_all_node_cost(self, route_cost):
        instructions = self.all_driving_instructions
        cost = route_cost
        for i in instructions:
            cost += self.get_cost_for_driving_in_node(str(i))
        return cost

    def update_ui_to_start_next_route(self):
        print("finished driving")
        self.ui.update_ui_to_start_again()

    def process_driving_instructions(self):
        self.all_driving_instructions.append("m")
        self.all_driving_instructions.reverse()
        self.next_instruction = str(self.all_driving_instructions.pop())

    def set_distance_and_draw_route_in_map(self, route):
        self.ui.set_distance(self.calc_real_range_from_cost_and_factor())
        self.ui.map.draw_route_in_map(route)
        self.ui.map.position_car_on_map(route[0], route[1])
        self.ui.update_map()

    def update_nodes_calc_routing_cost_and_get_next_instruction(self, route, cost):
        self.update_nodes_to_get_new_next_and_current_nodes(route[0], route[1])
        self.routing_cost = self.calc_all_node_cost(cost)
        self.next_instruction = str(self.all_driving_instructions.pop())

    def update_car_rotation(self):
        if len(self.server.current_rotation) != 0:
            car_standing = self.server.current_rotation.pop()
        else:
            print("empty")
            car_standing = 2
        print("Car rotation:", car_standing)
        if car_standing != 2:
            self.wait_for_crossing = True
        self.ui.map.update_rotation_of_car(car_standing)

    def update_car_position(self):
        if self.prev_distance < self.server.driven_distance:
            self.crossing_updated = False
            self.prev_distance = self.server.driven_distance
            self.ui.map.update_position_of_car_on_map(self.server.distance_difference_between_cur_and_prev_values)

    def check_if_car_is_at_node_position(self, route):
        if self.prev_distance < self.server.driven_distance and self.is_at_node == True:
            self.is_at_node = False
            self.crossing_updated = False
            route.pop()
            self.next_node = route[len(route)-1]
        new_route = route[:]
        print(self.prev_distance)
        # self.next_node_x == 0 and self.next_node_y == 0:
        current_node_x = self.ui.map.car.coordinates_of_all_node[route[len(route) - 1] - 1][0]
        current_node_y = self.ui.map.car.coordinates_of_all_node[route[len(route) - 1] - 1][1]
        if abs(self.ui.map.car.x_position - current_node_x) <= 4 and abs(
                self.ui.map.car.y_position - current_node_y) <= 4:
            self.is_at_node = True
            current_node = new_route.pop()
            self.ui.map.center_car_to_node(current_node)
            if self.wait_for_crossing:
                self.prev_distance += self.get_cost_for_driving_in_node("r")
                if self.crossing_updated == True:  # hier
                    self.prev_distance = self.prev_distance - self.get_cost_for_driving_in_node("g")
                else:
                    self.crossing_updated = True
                    # hier
                print("prev distance", self.prev_distance)
                self.wait_for_crossing = False
                if self.next_instruction != "g":
                    self.next_instruction = str(self.all_driving_instructions.pop())
                else:
                    self.ui.map.car.drives_true_route = False
            else:
                if self.crossing_updated == False:  # hier
                    self.prev_distance += self.get_cost_for_driving_in_node("g")
                    self.crossing_updated = True  # hier
                if self.next_instruction == "g":
                    self.next_instruction = str(self.all_driving_instructions.pop())
                else:
                    self.ui.map.car.drives_true_route = False
        return route

    def check_if_car_is_at_other_node_position(self, route):
        new_node_x = 0
        new_node_y = 0
        current_node_x = self.ui.map.car.coordinates_of_all_node[self.next_node - 1][0]
        current_node_y = self.ui.map.car.coordinates_of_all_node[self.next_node - 1][1]

        if not self.ui.map.car.drives_true_route:
            for i, (x, y) in enumerate(self.ui.map.car.coordinates_of_all_node):
                if abs(self.ui.map.car.x_position - x) <= 2 and abs(self.ui.map.car.y_position - y) <= 2:
                    if self.ui.map.car.x_position != current_node_x or self.ui.map.car.y_position != current_node_y:
                        self.ui.map.car.drives_true_route = True
                        return self.calc_new_route(i + 1)
        return route

    def calc_new_route(self, new_node):
        route, cost = self.get_route_from_algorithm(
            new_node, self.ui.get_end_point_for_navigation())
        self.all_driving_instructions = self.ui.get_driving_instructions_from_route(route)
        self.process_driving_instructions()

        self.update_nodes_calc_routing_cost_and_get_next_instruction(route, cost)
        self.ui.set_distance(self.calc_real_range_from_cost_and_factor())
        self.ui.map.draw_route_in_map(route)
        self.update_car_position()
        route.reverse()
        #route.pop()
        self.check_if_car_is_at_node_position(route)
        return route


if __name__ == "__main__":
    navigation = Navigation()
    navigation.init_navigation()
