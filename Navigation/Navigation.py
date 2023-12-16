#from PositioningSystem.positioningSystem import positioningSystem
from UserInterface.UserIntefaceForNavigation import userInterface
from Routing.routing import dijkstra
from configNavigation import *
from threading import Thread

class navigation:
    def __init__(self):
        self.ui = userInterface()
        #self.positioningSystem = positioningSystem(gyroAddress,hallPinForward,hallPinBackward)
        self.state = beforNavigationState
        self.routingCost = 0
        self.threadOne = 0

    def getRouteFromAlgorithm(self, startNode, endNode):
        return dijkstra(startNode, endNode, 1)  # Routen und Kosten berrechnung

    def getStateFromNavigation(self):
        return self.state

    def calcRealRangeFromCost(self, cost):

        return True

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

    def startApplication(self):
        try:
            while True:
                if self.ui.getClosedProgramBool():
                    self.threadOne._stop()
                    self.threadOne.join()
                match self.state:
                    case 1:
                        if self.ui.getIfUserInputIsReady():
                            self.state = afterInputState
                        else:
                            print("waiting for user input")
                    case 2:
                        print("calculating Route")
                        route, cost = self.getRouteFromAlgorithm(self.ui.getStartPointForNavigation(), self.ui.getEndPointForNavigation())
                        self.state = routingState
                        self.routingCost = cost
                        #self.routingCost = self.calcRealRangeFromCost(cost)
                        self.ui.setDistance(cost)
                        self.ui.drawRouteInMap(route)
                    case 3:
                        #if self.routingCost == self.positioningSystem.getDrivenDistanceFromSpeedometer():
                        #    self.state = drivingState
                        #else:
                        print("waitingForStart")
                    case 4:
                        print("finished driving")
                        self.state = drivingEndState
                    case 5:
                        print("next ride?")
                        self.state = beforNavigationState

                # print("Geschwindigkeit des Fahrzeugs: ",navigation.positioningSystem.speedometer.getSpeed(),"km/h")
                # print("Gefahrene Distanz: ", navigation.positioningSystem.speedometer.getDistance(),"m")
            print("hello")

        except KeyboardInterrupt:
            GPIO.cleanup()

if __name__ == "__main__":
    navigation = navigation()
    navigation.initNavigation()