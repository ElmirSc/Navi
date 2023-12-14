from PositioningSystem.positioningSystem import positioningSystem
from UserInterface.UserIntefaceForNavigation import userInterface
from Routing.routing import dijkstra
from configNavigation import *

class navigation:
    def __init__(self):
        self.ui = userInterface()
        self.positioningSystem = positioningSystem(gyroAddress,hallPinForward,hallPinBackward)

    def getRouteFromAlgorithm(self, startNode, endNode):
        return dijkstra(startNode, endNode, 1)  # Routen und Kosten berrechnung