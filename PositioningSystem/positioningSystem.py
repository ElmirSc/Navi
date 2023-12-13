from PositioningSystem.speedometer import speedometer
from mpu6050 import mpu6050

class positioningSystem:
    def __init__(self, mpu6050Address,hallPinForward,hallPinBackward):
        self.mpu6050 = mpu6050(mpu6050Address, gyroRange = 250)
        self.speedometer = speedometer(hallPinForward,hallPinBackward)
