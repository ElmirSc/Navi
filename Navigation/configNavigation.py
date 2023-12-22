import numpy as np

gyroAddress = 0x68
hallPinForward = 17
hallPinBackward = 27

#state manager
beforNavigationState = 1
afterInputState = 2
routingState = 3
drivingState = 4
drivingEndState = 5

nodeCoordsInMap = np.loadtxt("Navigation/nodeCordOnMap.txt")


