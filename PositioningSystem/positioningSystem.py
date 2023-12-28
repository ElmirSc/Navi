import sys
sys.path.append("/root")
import RPi.GPIO as GPIO
from speedometer import *
from own_mpu6050 import own_mpu6050
from positionigSystemConfig import *
from client import client

gyroAddress = 0x68
hallPinForward = 17
hallPinBackward = 27

class positioningSystem:
    def __init__(self,hallPinForward,hallPinBackward):
        self.mpu6050 = own_mpu6050(gyroRange=250)
        self.speedometer = speedometer(hallPinForward,hallPinBackward)
        self.defaultOrientationValue = self.mpu6050.getGyroZ()
        self.defaultOrientationValueRange = self.defaultOrientationValue * 0.1
        self.client = client()


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

    def init(self):
        self.speedometer.initSpeedometer()
        self.client.create_socket()

    def getSpeedFromSpeedometer(self):
        return self.speedometer.speed

    def getDrivenDistanceFromSpeedometer(self):
        return self.speedometer.distance

    def send_speed_distance_rotation_to_server(self):
        speed = self.getSpeedFromSpeedometer()
        print("Speed:",speed)
        dist = self.getSpeedFromSpeedometer()
        print("Distance:", dist)
        orientation = self.getOrientation()
        print("Orientation:", orientation)
        message = (str(speed)+" "+str(dist)+" "+str(orientation))
        self.client.send_message(message)


if __name__ == "__main__":
    pos_system = positioningSystem(hallPinForward, hallPinBackward)
    pos_system.init()
    try:
        while True:
            pos_system.send_speed_distance_rotation_to_server()
    except KeyboardInterrupt:
        pos_system.client.close_connection()
        GPIO.cleanup()