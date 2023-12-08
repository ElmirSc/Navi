from positioningSystem import positioningSystem
from UserIntefaceForNavigation import userInterface
from routing import dijkstra
from configNavigation import *

class navigation:
    def __init__(self):
        self.ui = userInterface()
        self.positioningSystem = positioningSystem(gyroAddress,hallPinForward,hallPinBackward)

    def getRouteFromAlgorithm(self):
        return dijkstra(1, 10, 1)  # Routen und Kosten berrechnung