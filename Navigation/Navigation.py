from PositioningSystem.positioningSystem import positioningSystem
from UserInterface.UserIntefaceForNavigation import userInterface
from Routing.routing import dijkstra, arc_list, node_list
from Navigation.configNavigation import *
from threading import Thread

class navigation:
    def __init__(self):
        self.ui = userInterface()
        self.positioningSystem = positioningSystem(gyroAddress,hallPinForward,hallPinBackward)
        self.state = beforNavigationState
        self.routingCost = 0
        self.threadOne = 0
        self.factor_for_real_distance = 1
        self.current_node = 0
        self.current_node_cost = 0
        self.next_node = 0
        self.old_cost = 0

    def getRouteFromAlgorithm(self, startNode, endNode):
        return dijkstra(startNode, endNode, 1)  # Routen und Kosten berrechnung

    def getStateFromNavigation(self):
        return self.state

    def calcRealRangeFromCost(self):
        return self.factor_for_real_distance * self.routingCost

    def calc_distance_to_drive(self,driven_distance):
        return self.calcRealRangeFromCost() - driven_distance

    def setNextState(self):
        match self.state:
            case 1:
                self.state = afterInputState
            case 2:
                self.state = routingState
            case 3:
                self.state = drivingState
            case 4:
                self.state = drivingEndState
            case 5:
                self.state = beforNavigationState

    def startUI(self):
        self.ui.initUI()

    def initNavigation(self):
        self.threadOne = Thread(target=self.startApplication)
        self.threadOne.start()
        self.startUI()
        self.threadOne.join()

    def startApplication(self):
        try:
            while True:
                if self.ui.getClosedProgramBool():  #zum schließen des ganzen programms
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
                        self.ui.position_car_on_map(0)
                        print(self.ui.getDrivingInstructionsFromRoute(route))
                    case 3:
                        if self.calc_distance_to_drive(self,self.positioningSystem.getDrivenDistanceFromSpeedometer()) == 0:
                          self.state = drivingState
                        else:
                          self.ui.setDistance(self.calc_distance_to_drive(self.positioningSystem.getDrivenDistanceFromSpeedometer()))
                          self.ui.updateSpeed(self,self.positioningSystem.getSpeedFromSpeedometer())
                          self.current_node_cost = self.positioningSystem.getDrivenDistanceFromSpeedometer() * self.factor_for_real_distance - self.old_cost
                          if self.positioningSystem.getDrivenDistanceFromSpeedometer() > self.find_next_cost_between_two_nodes():
                              update_nodes(self.next_node, get_next_node_from_route(self,route))
                              self.old_cost = self.current_node_cost
                              self.current_node_cost = 0
                          self.ui.update_position_of_car_on_map(self.current_node,self.next_node,0,self.current_node_cost,self.find_next_cost_between_two_nodes())
                        if 1 == 0:
                            print("waitingForStart")

                    case 4:
                        print("finished driving")
                        self.state = drivingEndState
                    case 5:
                        print("next ride?")
                        self.state = beforNavigationState
                        self.ui.updateUiToStartAgain()

        except KeyboardInterrupt:
            GPIO.cleanup()

    def update_nodes(self,new_current_node, new_next_node):
        self.next_node = new_next_node
        self.current_node = new_current_node

    def find_next_cost_between_two_nodes(self):
        max_edges_for_node = node_list[self.current_node + 1] - node_list[self.current_node]
        for i in range(node_list[self.current_node],node_list[self.current_node]+max_edges_for_node):
            edge = arc_list[i]
            if edge[0] == self.next_node:
                return edge[1]
        return 0

    def get_next_node_from_route(self,route):
        for i in range(0,len(route)):
            if route[i] == self.next_node:
                return route[i+1]
        return 0




if __name__ == "__main__":
    navigation = navigation()
    navigation.initNavigation()