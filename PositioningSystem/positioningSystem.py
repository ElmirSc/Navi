from PositioningSystem.speedometer import speedometer
from PositioningSystem.mpu6050 import mpu6050
from positionigSystemConfig import *

class positioningSystem:
    def __init__(self, mpu6050Address,hallPinForward,hallPinBackward):
        self.mpu6050 = mpu6050(mpu6050Address, gyroRange = 250)
        self.speedometer = speedometer(hallPinForward,hallPinBackward)
        self.defaultOrientationValue = self.mpu6050.getGyroZ()
        self.defaultOrientationValueRange = self.defaultOrientationValue * 0.1

    def getOrientation(self):
        orientation = None
        gyroZValue = self.mpu6050.getGyroZ()
        if gyroZValue < (self.defaultOrientationValue - self.defaultOrientationValueRange):
            orientation = turnLeft
        elif gyroZValue > (self.defaultOrientationValue + self.defaultOrientationValueRange):
            orientation = turnRight
        else:
            orientation = noTurn

        return orientation

    def getSpeedFromSpeedometer(self):
        return self.speedometer.speed

    def getDrivenDistanceFromSpeedometer(self):
        return self.speedometer.distance
