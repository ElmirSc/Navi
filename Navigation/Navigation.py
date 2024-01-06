import numpy as np
from UserInterface.UserIntefaceForNavigation import Userinterface
from Routing.routing import dijkstra, arc_list, node_list
from Navigation.configNavigation import *
from threading import Thread
from Navigation.server import Server


class Navigation:
    def __init__(self):
        self.ui = Userinterface()
        self.server = Server()
        self.current_state_of_app = before_navigation_state
        self.routing_cost = 0
        self.thread_one = 0
        self.factor_for_real_distance = 1
        self.current_node = 0
        self.current_node_cost = 0
        self.next_node = 0
        self.prev_driven_cost = 0
        self.total_cost_of_current_and_previous_nodes = 0
        self.node_coords_list = np.loadtxt("UserInterface/nodeCordOnMap.txt").astype(int)

    @staticmethod
    def get_route_from_algorithm(start_node, end_node):
        return dijkstra(start_node, end_node, 1)  # Routen und Kosten berrechnung

    def calc_real_range_from_cost_and_factor(self):
        return self.factor_for_real_distance * self.routing_cost

    def start_ui(self):
        self.ui.init_ui()

    def init_navigation(self):
        self.server.create_socket()
        self.server.set_socket_to_listen_mode()
        self.thread_one = Thread(target=self.start_application)
        self.thread_one.start()
        self.start_ui()
        self.thread_one.join()

    def start_application(self):
        try:
            route = None
            while True:
                if self.ui.get_closed_program_bool():  # zum schliessen des ganzen programms
                    break
                elif not self.ui.user_input_check_if_ready:  # erst wenn Input fertig ist wird state gesetzt
                    self.current_state_of_app = before_navigation_state

                match self.current_state_of_app:
                    case 1:
                        if self.ui.user_input_check_if_ready:
                            self.current_state_of_app = after_input_state
                    case 2:
                        route, cost = self.get_route_from_algorithm(
                            self.ui.get_start_point_for_navigation(), self.ui.get_end_point_for_navigation())
                        self.current_state_of_app = driving_state
                        self.update_nodes_to_get_new_next_and_current_nodes(route[0], route[1])
                        self.routing_cost = cost
                        self.ui.set_distance(self.calc_real_range_from_cost_and_factor())
                        self.ui.draw_route_in_map(route)
                        self.ui.position_car_on_map(route)
                        print(self.ui.get_driving_instructions_from_route(route))
                    case 3:
                        if self.server.accept_connection():
                            self.server.receive_data()
                            self.server.handle_data()
                            self.ui.calc_distance_to_drive(self.server.driven_distance)
                            self.ui.update_speed(self.server.current_speed * self.factor_for_real_distance)
                            if self.ui.distance_to_drive < 0:
                                self.current_state_of_app = driving_end_state
                                self.ui.update_speed(0)
                            self.current_node_cost = self.find_next_cost_between_two_nodes()
                            if self.server.driven_distance * self.factor_for_real_distance >= self.current_node_cost + self.prev_driven_cost:
                                self.update_nodes_to_get_new_next_and_current_nodes(self.next_node, self.get_next_node_from_route(route))
                                self.prev_driven_cost += self.current_node_cost
                            driven_distance_between_nodes = self.server.driven_distance * self.factor_for_real_distance - self.prev_driven_cost
                            self.ui.update_position_of_car_on_map(self.node_coords_list[self.current_node - 1],
                                                                  self.node_coords_list[self.next_node - 1],
                                                                  self.server.current_rotation, driven_distance_between_nodes,
                                                                  self.current_node_cost)
                        else:
                            print("Timeout gone!")
                    case 4:
                        print("finished driving")
                        self.ui.update_ui_to_start_again()

        except KeyboardInterrupt:
            print("progamm closed!")

    def update_nodes_to_get_new_next_and_current_nodes(self, new_current_node, new_next_node):
        self.next_node = new_next_node
        self.current_node = new_current_node

    def find_next_cost_between_two_nodes(self):
        max_edges_for_node = node_list[self.current_node] - node_list[self.current_node - 1]
        for i in range(node_list[self.current_node - 1], node_list[self.current_node - 1] + max_edges_for_node):
            edge = arc_list[i - 1]
            if edge[0] == self.next_node:
                return int(edge[1])
        return 0

    def get_next_node_from_route(self, route):
        for i in range(0, len(route)):
            if i == len(route) - 1:
                return route[i]
            if route[i] == self.next_node:
                return route[i + 1]
        return 0


if __name__ == "__main__":
    navigation = Navigation()
    navigation.init_navigation()
