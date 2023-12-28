import sys
sys.path.append("/root")
import RPi.GPIO as GPIO
from speedometer import speedometer
from mpu6050 import mpu6050
from positionigSystemConfig import *
from client import client_for_connection

gyroAddress = 0x68
hallPinForward = 17
hallPinBackward = 27

class positioningSystem:
    def __init__(self, mpu6050Address,hallPinForward,hallPinBackward):
        self.mpu6050 = mpu6050(mpu6050Address, gyroRange = 250)
        self.speedometer = speedometer(hallPinForward,hallPinBackward)
        self.defaultOrientationValue = self.mpu6050.getGyroZ()
        self.defaultOrientationValueRange = self.defaultOrientationValue * 0.1
        self.client = client_for_connection.create_socket()

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

    def send_speed_distance_rotation_to_server(self):
        speed = self.getSpeedFromSpeedometer()
        dist = self.getSpeedFromSpeedometer()
        orientation = self.getOrientation()
        message = str(speed+" "+dist+" "+orientation)
        self.client.send_message(message)


if __name__ == "__main__":
    pos_system = positioningSystem(gyroAddress,hallPinForward,hallPinBackward)
    try:
        while True:
            pos_system.send_speed_distance_rotation_to_server()
    except KeyboardInterrupt:
        pos_system.client.close_connection()
        GPIO.cleanup()