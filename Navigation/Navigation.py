#from PositioningSystem.positioningSystem import positioningSystem
from UserInterface.UserIntefaceForNavigation import userInterface
from Routing.routing import dijkstra, arc_list, node_list
from Navigation.configNavigation import *
from threading import Thread
from Navigation.server import server

class navigation:
    def __init__(self):
        self.ui = userInterface()
        #self.positioningSystem = positioningSystem(gyroAddress,hallPinForward,hallPinBackward)
        self.state = beforNavigationState
        self.routingCost = 0
        self.threadOne = 0
        self.factor_for_real_distance = 1
        self.current_node = 0
        self.current_node_cost = 0
        self.next_node = 0
        self.old_cost = 0
        self.server = server()
        self.total_cost_of_current_and_previous_nodes = 0
        self.node_coords_list = np.loadtxt("UserInterface/nodeCordOnMap.txt").astype(int)

    def getRouteFromAlgorithm(self, startNode, endNode):
        return dijkstra(startNode, endNode, 1)  # Routen und Kosten berrechnung

    def getStateFromNavigation(self):
        return self.state

    def calcRealRangeFromCost(self):
        return self.factor_for_real_distance * self.routingCost

    def calc_distance_to_drive(self,driven_distance):
        return self.calcRealRangeFromCost() - driven_distance

    def setNextState(self):
        if self.state == 1:
            self.state = afterInputState
        elif self.state == 2:
            self.state = routingState
        elif self.state == 3:
            self.state = drivingState
        elif self.state == 4:
            self.state = drivingEndState
        elif self.state == 5:
            self.state = beforNavigationState


    def startUI(self):
        self.ui.initUI()

    def initNavigation(self):
        self.server.create_socket()
        self.server.set_socket_to_listen_mode()
        self.threadOne = Thread(target=self.startApplication)
        self.threadOne.start()
        self.startUI()
        self.threadOne.join()

    def startApplication(self):
        try:
            while True:
                if self.ui.getClosedProgramBool():  #zum schliessen des ganzen programms
                    break
                elif not self.ui.userInputIsReady:  #erst wenn Input fertig ist wird state gesetzt
                    self.state = beforNavigationState

                match self.state:
                    case 1:
                        if self.ui.getIfUserInputIsReady():
                            self.state = afterInputState
                    case 2:
                        route, cost, drivingInstructions = self.getRouteFromAlgorithm(self.ui.getStartPointForNavigation(), self.ui.getEndPointForNavigation())
                        self.state = routingState
                        self.update_nodes(route[0], route[1])
                        self.routingCost = cost
                        self.ui.setDistance(self.calcRealRangeFromCost())
                        self.ui.drawRouteInMap(route)
                        #funktion machen die anhand der nodes auswählt wie die anfangsrotation des Fahrzeugs ist
                        self.ui.position_car_on_map(4)
                        print(self.ui.getDrivingInstructionsFromRoute(route))
                    case 3:
                        if self.server.accept_connection():
                            self.server.receive_data()
                            self.server.handle_data()
                            self.ui.calc_distance_to_drive(self.server.dist)
                            self.ui.updateSpeed(self.server.speed * self.factor_for_real_distance)
                            if self.ui.dist_to_drive == 0:
                                self.state = drivingState
                                self.ui.updateSpeed(0)
                            self.current_node_cost = self.find_next_cost_between_two_nodes()
                            # self.current_node_cost = self.server.dist * self.factor_for_real_distance - self.old_cost
                            if self.server.dist * self.factor_for_real_distance >= self.current_node_cost + self.old_cost:
                                print(self.current_node_cost)
                                self.update_nodes(self.next_node, self.get_next_node_from_route(route))
                                self.old_cost += self.current_node_cost
                            driven_distance_between_nodes = self.server.dist * self.factor_for_real_distance - self.old_cost
                            self.ui.update_position_of_car_on_map(self.node_coords_list[self.current_node-1],self.node_coords_list[self.next_node-1],self.server.rotation,driven_distance_between_nodes,self.current_node_cost)

                    case 4:
                        print("finished driving")
                        self.ui.updateUiToStartAgain()

        except KeyboardInterrupt:
            print("progamm closed!")

#

    def start_server(self):
        return

    def update_nodes(self,new_current_node, new_next_node):
        self.next_node = new_next_node
        self.current_node = new_current_node

    def find_next_cost_between_two_nodes(self):
        max_edges_for_node = node_list[self.current_node] - node_list[self.current_node - 1]
        for i in range(node_list[self.current_node - 1], node_list[self.current_node - 1] + max_edges_for_node):
            edge = arc_list[i-1]
            if edge[0] == self.next_node:
                return int(edge[1])
        return 0

    def get_next_node_from_route(self,route):
        for i in range(0,len(route)):
            if i == len(route)-1:
                return route[i]
            if route[i] == self.next_node:
                return route[i+1]
        return 0




if __name__ == "__main__":
    navigation = navigation()
    navigation.initNavigation()