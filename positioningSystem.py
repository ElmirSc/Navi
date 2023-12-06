from speedometer import speedometer
from gyroskop import gyro

class positioningSystem:
    def __init__(self, gyroAddress,hallPinForward,hallPinBackward):
        self.gyroskop = gyro(gyroAddress)
        self.speedometer = speedometer(hallPinForward,hallPinBackward)
